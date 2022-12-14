3 Personas
- Buyer
- Seller
- Admin

Admins have the ability to ban sellers and buyers.

A Buyer and Seller profile is created for each user of the platform, similar to how most online shopping platforms work. Each of these two profiles have their own UserInfo entry that stores their basic info.

With their seller profile, users can list items for sale in a specific quantity for a specific price. In doing so, they add to the Products database table. 

A Buyer can purchase one of these items by placing an order, creating a new entry in the orders table. If this order can be met, it then subtracts the quantity from the products table's entry corresponding to that order. To get order or sale history for a buyer or seller, we simply look through the order database and filter by the orders who's buyer or seller id equals that of the buyer/seller we are looking at.

Video Link: https://drive.google.com/file/d/1ery5UWAWw0ekRND9Totq5RkVDuLzkOUO/view?usp=sharing
