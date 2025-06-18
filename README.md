# Run locally 
### With Docker
  1. Install docker and docker-compose on your system
  2. Clone the repository using ```git clone https://github.com/sagarmamodia/dupatta-house-backend.git```
  3. Build the app using ```docker-compose up --build```
  4. Run the app using ```docker-compose up```
  5. To stop use ```docker-compose stop```
  6. To restart use ```docker-compose start```
  7. To remove the containers ```docker-compose down```

### Without Docker 
  1. Make sure your system have python 3.11 or higher installed.
  2. Clone the repository using ```git clone https://github.com/sagarmamodia/dupatta-house-backend.git```.
  3. Run ```pip install -r requirements.txt``` to install the dependencies.
  4. Run the app using ```python manage.py runserver```

# API Docs
1. POST auth/register/
   - Create an account
   - Expected JSON data
   ```
   {
     username: <value>,
     password: <value>,
     email: <value>
   }
   ```
2. POST auth/token/
   - Login into your account and get access and refresh token
   - Expected JSON data
   ```
   {
     username: <value>,
     password: <value>,
     email: <value>
   }
   ```
3. POST auth/token/refresh/
   - Get a new access token
   - Expected JSON data
   ```
   {
     refresh: <value>,
     access: <value>
   }
   ```
4. GET api/products/
   - Get a list of all the products from database

5. GET api/cart/
   - Get all the products in the cart of logged in user.
   - **This require access token in Bearer header**.

6. POST api/cart/add/
   - Add a product to the cart of logged in user
   - **This require access token in Bearer header**.
   - Expected JSON data
   ```
   {
      product: <id>,
      quantity: <value>
   }
   ```

6. POST api/orders/create/
   - Create an order in database
   - **This require access token in Bearer header**.
   - Expected JSON data
   ```
   {
     delivery_address: <value>,
     pincode: <value>,
     contact_number: <value>,
     items: [
         {
           product: <id>,
           quantity: <value>
         },
         ...
     ]
   }
   ```
7. POST api/payments/create/
   - To place an order you client must initiate a payment session which will **return a razorpay order_id.**
   - **This required access token in Bearer header**.
   - Expected JSON data
   ```
   {
     order: <order_id>
   }
   ```
8. POST api/payments/callback/
   - After making a successful payment on razorpay the client must call this callback to register the payment with the backend otherwise backend would be unaware that the payment has been made.
   - **This requires access token in Bearer header**.
   - Expected JSON data
   ```
   {
    razorpay_order_id: <value>,
   razorpay_payment_id: <value>,
   razorpay_signature: <value>
   }
   ```

9. GET api/orders/
   - Get a list of all the orders made by the logged in user.
   - **This requires access token in Bearer header**
