import exifread


def check_image_metadata(image_file):
    """
    Extract EXIF metadata and perform
    geo-tag fraud analysis
    """

    try:

        tags = exifread.process_file(image_file)

        image_date = tags.get("EXIF DateTimeOriginal")
        modified_date = tags.get("Image DateTime")

        gps_latitude = tags.get("GPS GPSLatitude")
        gps_longitude = tags.get("GPS GPSLongitude")

        device_model = tags.get("Image Model")

        result = {}

        # -----------------------------------
        # Metadata Extraction
        # -----------------------------------
        result["Image Date"] = (
            str(image_date)
            if image_date
            else "Not Available"
        )

        result["Modified Date"] = (
            str(modified_date)
            if modified_date
            else "Not Available"
        )

        result["Device Model"] = (
            str(device_model)
            if device_model
            else "Unknown Device"
        )

        # -----------------------------------
        # Geo-tag Verification
        # -----------------------------------
        if gps_latitude and gps_longitude:

            result["Geo-tag"] = "Found ✅"

            result["Latitude"] = str(gps_latitude)
            result["Longitude"] = str(gps_longitude)

        else:

            result["Geo-tag"] = "Missing ❌"

            result["Latitude"] = "Not Available"
            result["Longitude"] = "Not Available"

        # -----------------------------------
        # Fraud Hint Logic
        # -----------------------------------
        fraud_hints = []

        if not image_date:
            fraud_hints.append(
                "⚠ Original capture date missing"
            )

        if not gps_latitude:
            fraud_hints.append(
                "⚠ No geo-location found"
            )

        if modified_date and image_date:

            if str(modified_date) != str(image_date):

                fraud_hints.append(
                    "⚠ Image may have been edited"
                )

        # Final fraud analysis
        if not fraud_hints:

            result["Fraud Hint"] = "Looks Normal ✅"

            result["Fraud Risk"] = "Low Fraud Risk"

        else:

            result["Fraud Hint"] = fraud_hints

            if len(fraud_hints) >= 2:
                result["Fraud Risk"] = "High Fraud Risk"

            else:
                result["Fraud Risk"] = "Medium Fraud Risk"

        return result

    except Exception as e:

        return {
            "Error": str(e),
            "Fraud Risk": "Unknown"
        }