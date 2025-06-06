import hmac 
import hashlib 

razorpay_order_id = "razorpay_id_2_0.013801637925781263"
razorpay_payment_id = "razorpay_payment_id" 
razorpay_key_secret = "razorpay_key_secret"
body = f"{razorpay_order_id}|{razorpay_payment_id}"
generated_signature = hmac.new(
    razorpay_key_secret.encode(),
    body.encode(),
    hashlib.sha256
).hexdigest()

print(generated_signature)



