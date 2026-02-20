import json
import numpy as np
import pandas as pd
import pickle
from pathlib import Path

class LocationPriorBuilder:
    """
    Builds a probability matrix:
    Rows    = Indian states (36 states + UTs)
    Columns = Bird species (all species in your dataset)
    Value   = Probability that this species appears in this state

    Example:
    Great_Hornbill in Kerala  = 0.95  (very common there)
    Great_Hornbill in Rajasthan = 0.02  (almost never seen there)
    House_Sparrow in any state = 0.90  (found everywhere)
    """

    def __init__(self, data_dir='dataset/location_data', label_encoder_path='backend/models/label_encoder.pkl'):
        self.data_dir = Path(data_dir)

        # Load label encoder so we know all species and their index numbers
        with open(label_encoder_path, 'rb') as f:
            self.label_encoder = pickle.load(f)

        self.species_list = list(self.label_encoder.classes_)
        self.num_species = len(self.species_list)

        # Load all location data files
        with open(self.data_dir / 'india_states_species.json') as f:
            self.state_species_data = json.load(f)

        with open(self.data_dir / 'state_neighbors.json') as f:
            self.state_neighbors = json.load(f)

        with open(self.data_dir / 'seasonal_presence.json') as f:
            self.seasonal_data = json.load(f)

        self.states_list = list(self.state_species_data.keys())
        self.num_states = len(self.states_list)

    def build_base_prior_matrix(self):
        """
        Creates the main matrix.
        For each state, each species gets a score:
        - 0.95 if the species is endemic (only found here)
        - 0.80 if the species is confirmed present in this state
        - 0.10 if the species is present in a neighboring state (border effect)
        - 0.01 if the species is not recorded here at all (near-zero but not zero,
                because rare sightings do happen — never make probability exactly 0)
        """
        # Start with a matrix of all near-zeros
        # Shape: (num_states, num_species)
        prior_matrix = np.full((self.num_states, self.num_species), 0.01)

        for state_idx, state_name in enumerate(self.states_list):
            state_data = self.state_species_data[state_name]
            confirmed_species = set(state_data['species'])
            endemic_species = set(state_data.get('endemic_species', []))

            # Get all neighboring states' species
            neighbor_states = self.state_neighbors.get(state_name, [])
            neighbor_species = set()
            for neighbor in neighbor_states:
                if neighbor in self.state_species_data:
                    neighbor_species.update(self.state_species_data[neighbor]['species'])

            for species_idx, species_name in enumerate(self.species_list):
                if species_name in endemic_species:
                    # Endemic = found ONLY in this state or very few places
                    prior_matrix[state_idx, species_idx] = 0.95

                elif species_name in confirmed_species:
                    # Confirmed present in this state
                    prior_matrix[state_idx, species_idx] = 0.80

                elif species_name in neighbor_species:
                    # Not in this state officially but in a neighboring state
                    # Could appear near borders
                    prior_matrix[state_idx, species_idx] = 0.10

                # else it stays 0.01 (very unlikely but not impossible)

        return prior_matrix

    def apply_seasonal_adjustment(self, prior_matrix, month):
        """
        Adjusts the matrix for the current month.
        If a bird is migratory and this month it should not be here,
        reduce its probability significantly.
        """
        adjusted = prior_matrix.copy()

        for species_name, seasonal_info in self.seasonal_data.items():
            if species_name not in self.species_list:
                continue

            species_idx = self.species_list.index(species_name)
            resident_months = seasonal_info['resident_months']

            if month not in resident_months:
                # This bird is not present this month — reduce to near zero
                adjusted[:, species_idx] *= 0.05

        return adjusted

    def normalize_matrix(self, matrix):
        """
        Normalize each row so values are on a comparable scale.
        We do NOT normalize to sum=1 because we want to use this as
        a multiplier on top of the model's output, not replace it.
        We normalize each row to have max value = 1.0
        """
        row_max = matrix.max(axis=1, keepdims=True)
        row_max[row_max == 0] = 1  # Avoid division by zero
        return matrix / row_max

    def build_and_save(self, output_path='backend/models/location_prior_matrix.pkl'):
        """Run everything and save the final matrix"""
        print("Building base prior matrix...")
        matrix = self.build_base_prior_matrix()

        print("Normalizing matrix...")
        matrix = self.normalize_matrix(matrix)

        # Save everything needed for inference
        location_prior_data = {
            'matrix': matrix,                    # The actual numpy array
            'states_list': self.states_list,     # State name → row index mapping
            'species_list': self.species_list,   # Species name → column index mapping
            'state_to_idx': {s: i for i, s in enumerate(self.states_list)},
            'seasonal_data': self.seasonal_data
        }

        with open(output_path, 'wb') as f:
            pickle.dump(location_prior_data, f)

        print(f"Location prior matrix saved! Shape: {matrix.shape}")
        print(f"States: {self.num_states}, Species: {self.num_species}")
        return location_prior_data


# Run this after training — after label_encoder.pkl is created
if __name__ == '__main__':
    builder = LocationPriorBuilder()
    builder.build_and_save()