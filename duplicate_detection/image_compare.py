from PIL import Image
import imagehash
import os


def compare_with_database(uploaded_image, database_folder):
    """
    Compare uploaded plantation image
    with all database images.

    Returns:
    - best similarity
    - duplicate status
    - fraud risk
    - matched image
    """

    uploaded_hash = imagehash.average_hash(
        Image.open(uploaded_image)
    )

    best_similarity = 0
    matched_image = None

    # Scan all images in database
    for file_name in os.listdir(database_folder):

        db_image_path = os.path.join(
            database_folder,
            file_name
        )

        try:
            db_hash = imagehash.average_hash(
                Image.open(db_image_path)
            )

            difference = uploaded_hash - db_hash

            similarity = max(
                0,
                100 - (difference * 5)
            )

            # Store best match
            if similarity > best_similarity:
                best_similarity = similarity
                matched_image = file_name

        except:
            continue

    # Final classification
    if best_similarity >= 90:
        status = "Likely Duplicate"
        risk = "High Fraud Risk"

    elif best_similarity >= 70:
        status = "Possibly Similar"
        risk = "Medium Fraud Risk"

    else:
        status = "Different Image"
        risk = "Low Fraud Risk"

    return (
        best_similarity,
        status,
        risk,
        matched_image
    )