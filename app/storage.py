import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError

load_dotenv()

# === Config ===
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("R2_BUCKET_NAME")

# === Init client R2 ===
try:
    r2_client = boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name=""
    )
except BotoCoreError as e:
    raise RuntimeError(f"❌ Errore durante l'inizializzazione del client R2: {str(e)}")


# === Upload Function ===
def upload_file_to_r2(file_bytes: bytes, filename: str, chat_id: str) -> str:
    """
    Carica un file su Cloudflare R2 e restituisce un URL firmato valido per 1 ora.
    """
    key = f"{chat_id}/{filename}"

    try:
        # Upload del file
        r2_client.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=file_bytes
        )
    except ClientError as e:
        raise RuntimeError(f"❌ Errore durante l'upload su R2: {e.response['Error']['Message']}")
    except Exception as e:
        raise RuntimeError(f"❌ Errore generico durante upload R2: {str(e)}")

    try:
        # Genera presigned URL
        presigned_url = r2_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': key},
            ExpiresIn=3600  # secondi
        )
        return presigned_url
    except ClientError as e:
        raise RuntimeError(f"❌ Errore durante la generazione del presigned URL: {e.response['Error']['Message']}")
    except Exception as e:
        raise RuntimeError(f"❌ Errore generico nella generazione dell'URL firmato: {str(e)}")
