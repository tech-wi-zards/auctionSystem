import streamlit as st
import sqlite3
import pandas as pd

#databases connections

conn=sqlite3.connect('database.db')
c=conn.cursor()

## for users data
def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY,password TEXT, account TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS sellersdata(product_name TEXT PRIMARY KEY, product_amount TEXT,username TEXT,CONSTRAINT fk_userstable FOREIGN KEY(username) REFERENCES userstable(username))')
    c.execute('CREATE TABLE IF NOT EXISTS buyersdata(product_name TEXT,amt TEXT,username TEXT,CONSTRAINT fk_userstable FOREIGN KEY(username) REFERENCES userstable(username),CONSTRAINT sellersdata FOREIGN KEY(product_name) REFERENCES sellersdata(product_name))')

def add_userdata(username,password,accounttype):
    c.execute('INSERT INTO userstable(username,password,account) VALUES (?,?,?)',(username,password,accounttype))
    conn.commit()

def login_user(username,password,accounttype):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ? AND account = ?',(username,password,accounttype))
    data= c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data=c.fetchall()
    return data

##### for seller data
def add_sellersdata(productName,productPrice,username):
    c.execute('INSERT INTO sellersdata(product_name,product_amount,username) VALUES (?,?,?)',(productName,productPrice,username))
    conn.commit()

def view_all_sellersdata():
    c.execute('SELECT * FROM sellersdata')
    data=c.fetchall()
    return data

def view_all_seller_products_of_user(username):
    c.execute('SELECT * FROM sellersdata WHERE username =?',(username,))
    data=c.fetchall()
    return data

def get_seller_products_names_of_the_user(username):
    c.execute('SELECT (product_name) FROM sellersdata WHERE username =?',(username,))
    data=c.fetchall()
    return data

## for buyers data
def add_buyerdata(productName,bidamt,name):
    c.execute('INSERT INTO buyersdata(product_name,amt,username) VALUES (?,?,?)',(productName,bidamt,name))
    conn.commit()

def view_buyer_products_of_user(name):
    c.execute('SELECT * FROM buyersdata WHERE username =?',(name,))
    data=c.fetchall()
    return data

def view_all_buyersdata():
    c.execute('SELECT * FROM buyersdata')
    data=c.fetchall()
    return data

def main():

    st.title("ONLINE AUCTION SYSTEM")
    menu=["Home","Admin Login","Seller Login","Buyer Login","SignUp"]
    choice= st.sidebar.selectbox("Menu",menu)
    if choice=="Home":
        st.subheader("Home")

    elif choice== "Seller Login":## seller login part
        st.subheader("Login Section")
        username=st.sidebar.text_input("User Name")
        password=st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            create_tables()
            accountType="Seller"
            result=login_user(username,password,accountType)
            if result:
                st.success("Logged in as {}".format(username))

                task=st.selectbox("Task",["select the options","Add New Product","View your products","View product details"])

                if task =="Add New Product":
                    st.subheader("Add your Product Details here")
                    product_name=st.text_input("Enter Product Name")
                    product_minimum_price=st.text_input("Enter the minimum price to buy this product")
                    if st.button("Submit"):
                        add_sellersdata(product_name,product_minimum_price,username)
                        st.success("You have created a product")
                        st.info("Go to view your products to see ur updated products")


                elif task =="View your products":
                    st.subheader("View your products")
                    productSearch=view_all_seller_products_of_user(username)
                    pandas_db = pd.DataFrame(productSearch, columns=["product name", "product price", "username"])
                    st.dataframe(pandas_db)

                elif task=="View product details":
                    st.subheader("View product details")
                    Products = get_seller_products_names_of_the_user(username)
                    #pandas_db = pd.DataFrame(Products, columns=["product name", "product price", "username"])
                    pandas_db = pd.DataFrame(Products, columns=["product name"])
                    st.dataframe(pandas_db)

                    #stringProducts=str(Products)
                    #stringProducts=stringProducts.split(',')
                    #ProductSelection = st.selectbox("product selection", ["select the options",stringProducts])


            else:
                st.warning("Incorrect Username/password")

    elif choice== "Buyer Login":## buyer login part
        st.subheader("Login Section")
        username=st.sidebar.text_input("User Name")
        password=st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            create_tables()
            accountType="Buyer"
            result=login_user(username,password,accountType)
            if result:
                st.success("Logged in as {}".format(username))

                task=st.selectbox("Task",["select the options","Apply","View products","View your products"])

                if task =="Apply":
                    st.subheader("Enter the required details for applying for that auction")
                    #name=st.text_input("Enter your name")
                    product_name=st.text_input("Enter Product Name")
                    product_price=st.text_input("Enter the amount to purchase the product")
                    if st.button("Submit"):
                        add_buyerdata(product_name,product_price,username)
                        st.success("You have created a product")
                        st.info("Go to view your products to see ur updated products")


                elif task =="View products":
                    st.subheader("products available for auction")
                    allProducts=view_all_sellersdata()
                    pandas_db=pd.DataFrame(allProducts,columns=["product name","product price","username"])
                    st.dataframe(pandas_db)

                elif task=="View your products":
                    st.subheader("View product details")
                    productSearch = view_buyer_products_of_user(username)
                    pandas_db = pd.DataFrame(productSearch, columns=["product name", "product price","username"])
                    st.dataframe(pandas_db)

            else:
                st.warning("Incorrect Username/password")

    elif choice== "Admin Login":
        st.subheader("Login Section")
        username=st.sidebar.text_input("User Name")
        password=st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            #if password =="admin" and username=="admin":
            create_tables()
            accountType = "admin"
            result = login_user(username, password, accountType)
            if result:
                st.success("Logged in as {}".format(username))

                task=st.selectbox("Task",["All Auctions","All Buyers","Profiles"])
                if task =="All Auctions":
                    st.subheader("Auctions")
                    if username=="admin" and password=="admin":
                        user_result=view_all_sellersdata()
                        #printing the database in the form of the pandas dataframe
                        pandas_db=pd.DataFrame(user_result,columns=["ProductName","productAmount","Username"])
                        st.dataframe(pandas_db)
                    else:
                        st.warning("only Admin Dept can access to this sorry for the inconvince....")

                elif task =="All Buyers":
                    st.subheader("Buyers")
                    if username=="admin" and password=="admin":
                        user_result=view_all_buyersdata()
                        #printing the database in the form of the pandas dataframe
                        pandas_db=pd.DataFrame(user_result,columns=["productNames","amt","usernames"])
                        st.dataframe(pandas_db)
                    else:
                        st.warning("only Admin Dept can access to this sorry for the inconvince....")

                elif task =="Profiles":
                    if username=="admin" and password=="admin":
                        st.subheader("User Profiles")
                        user_result=view_all_users()
                        #printing the database in the form of the pandas dataframe
                        pandas_db=pd.DataFrame(user_result,columns=["Username","Password","accountType"])
                        st.dataframe(pandas_db)
                    else:
                        st.warning("only Admin Dept can access to this sorry for the inconvince....")
            else:
                st.warning("Incorrect Username/password")



    elif choice=="SignUp":
        st.subheader("Create New Account")
        new_user=st.text_input("User Name")
        new_password=st.text_input("Password",type='password')

        account_type_choice=st.selectbox("Account Type",["Seller","Buyer","admin"])
        if account_type_choice=="Seller":
            account_type="Seller"

        elif account_type_choice=="Buyer":
            account_type="Buyer"
        else:
            account_type="admin"
        if st.button("SignUp"):
            create_tables()
            add_userdata(new_user,new_password,account_type)
            st.success("You have created an account")
            st.info("Go to Login to login")


if __name__=='__main__':
    main()