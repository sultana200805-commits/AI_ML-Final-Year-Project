@router.post("/recognize/fusion")
async def recognize_bird_fusion(
    audio: UploadFile = File(...),
    image: UploadFile = File(...),
    # Location inputs — ALL OPTIONAL
    latitude: Optional[float]  = Form(None),
    longitude: Optional[float] = Form(None),
    state_name: Optional[str]  = Form(None),   # User manually picked state
    use_location: Optional[bool] = Form(True), # User can turn off location filter
):
    audio_bytes = await audio.read()
    image_bytes = await image.read()

    # Resolve which state to use
    resolved_state = None

    if use_location:
        location_service = LocationService()

        if state_name:
            # User manually selected state from dropdown — use that
            resolved_state = location_service.get_state_from_name(state_name)

        elif latitude is not None and longitude is not None:
            # User shared GPS — auto-detect state
            resolved_state = await location_service.get_state_from_coordinates(
                latitude, longitude
            )

        # If neither — resolved_state stays None and filter is skipped

    # Get current month for seasonal filtering
    current_month = datetime.now().month

    predictions = prediction_service.predict_fusion(
        audio_bytes=audio_bytes,
        image_bytes=image_bytes,
        state_name=resolved_state,
        month=current_month if resolved_state else None,
        top_k=5
    )

    top_species = predictions[0]['species_code']
    bird_details = await bird_db.get_bird_details(top_species)

    # Build the response
    location_info = {}
    if resolved_state:
        location_info = {
            "filter_applied": True,
            "detected_state": resolved_state,
            "filter_strength": "30% location influence",
            "seasonal_filter": True,
            "month_checked": current_month
        }
    else:
        location_info = {
            "filter_applied": False,
            "reason": "No location provided or location filter turned off"
        }

    return JSONResponse({
        "success": True,
        "recognition_type": "audio+image+location_fusion",
        "top_prediction": {**predictions[0], **bird_details},
        "alternatives": predictions[1:],
        "location_info": location_info,
        "user_coordinates": {
            "latitude": latitude,
            "longitude": longitude
        }
    })