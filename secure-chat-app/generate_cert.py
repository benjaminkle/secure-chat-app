from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import os

os.makedirs("certificates", exist_ok=True)

key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "CA"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Ontario"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Toronto"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Secure Chat App"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

now = datetime.datetime.now(datetime.UTC)

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(now)
    .not_valid_after(now + datetime.timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
    )
    .sign(key, hashes.SHA256())
)

with open("certificates/key.pem", "wb") as f:
    f.write(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        )
    )

with open("certificates/cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("SSL certificate and key generated successfully.")