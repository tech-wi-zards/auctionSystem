import streamlit as st
import sqlite3
import pandas as pd
import requests
import io
from PIL import Image
from cryptography.fernet import Fernet

def modification(t):
    te = ""
    for i in t:
        for j in i:
            te = te + j + ","

    lo = te.split(",")
    lo.remove("")
    return (lo)

def convertToBinaryData(filename):
    # Convert digital data to binary format
    blobData = filename.read()
    return blobData

def url_image_loader(url):
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    img = Image.open(image_bytes)
    st.image(img)

#databases connections
conn=sqlite3.connect('database.db')
c=conn.cursor()


def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY,password BLOB, account TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS sellersdata(product_name TEXT PRIMARY KEY, product_amount TEXT,username TEXT,CONSTRAINT fk_userstable FOREIGN KEY(username) REFERENCES userstable(username))')
    c.execute('CREATE TABLE IF NOT EXISTS buyersdata(product_name TEXT,amt TEXT,username TEXT,status TEXT,CONSTRAINT fk_userstable FOREIGN KEY(username) REFERENCES userstable(username),CONSTRAINT sellersdata FOREIGN KEY(product_name) REFERENCES sellersdata(product_name))')
    c.execute('CREATE TABLE IF NOT EXISTS imgtable(product_name TEXT PRIMARY KEY, img BLOB,CONSTRAINT sellersdata FOREIGN KEY(product_name) REFERENCES sellersdata(product_name))')

def drop_all_tables():
    c.execute("DROP TABLE userstable")
    c.execute("DROP TABLE sellersdata")
    c.execute("DROP TABLE buyersdata")
    c.execute("DROP TABLE imgtable")

## for users data
def add_userdata(username,password,accounttype):
    c.execute('INSERT INTO userstable(username,password,account) VALUES (?,?,?)',(username,password,accounttype))
    conn.commit()

def login_user(username,password,accounttype):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ? AND account = ?',(username,password,accounttype))
    data= c.fetchall()
    return data

def view_all_usersdata():
    c.execute('SELECT * FROM userstable')
    data=c.fetchall()
    return data

def view_user(userName):
    c.execute('SELECT (username) FROM userstable WHERE username =?',(userName,))
    data=c.fetchall()
    return data

def get_password(userName,account):
    c.execute('SELECT (password) FROM userstable WHERE username =? AND account =?',(userName,account))
    data=c.fetchall()
    return data

# def delete_account(userName,password,account):
#     c.execute('DELETE FROM userstable WHERE username=? AND password=? AND account =?',(userName,password,account))
#     #c.execute('DELETE FROM buyers')
#     conn.commit()

##### for imgtable
def add_imgdata(productName,imgData):
    c.execute('INSERT INTO imgtable(product_name,img) VALUES (?,?)',(productName,imgData))
    conn.commit()

def get_imgdata(productName):
    c.execute('SELECT (img) FROM imgtable WHERE product_name =?',(productName,))
    data=c.fetchall()
    #print("done getting the img data")
    return data

def delete_imgdata_productname(productName):
    c.execute('DELETE FROM imgtable WHERE product_name =?',(productName,))
    conn.commit()

def get_productNames_imgdata():
    c.execute('SELECT (product_name) FROM imgtable')
    data = c.fetchall()
    return data

##### for seller data
def add_sellersdata(productName,productPrice,username):
    c.execute('INSERT INTO sellersdata(product_name,product_amount,username) VALUES (?,?,?)',(productName,productPrice,username))
    conn.commit()

def view_all_sellersdata():
    c.execute('SELECT * FROM sellersdata')
    data=c.fetchall()
    return data

def view_all_productnames_sellerdata():
    c.execute('SELECT (product_name) FROM sellersdata')
    data=c.fetchall()
    return data

def view_all_seller_products_of_user(username):
    c.execute('SELECT product_name,product_amount FROM sellersdata WHERE username =?',(username,))
    data=c.fetchall()
    return data

def check_product_name_based_on_productName(productname):
    c.execute('SELECT (product_name) FROM sellersdata WHERE product_name =?',(productname,))
    data=c.fetchall()
    return data

def get_seller_products_names_of_the_user(username):
    c.execute('SELECT (product_name) FROM sellersdata WHERE username =?',(username,))
    data=c.fetchall()
    return data

def get_seller_product_amount_of_the_user(productName):
    c.execute('SELECT (product_amount) FROM sellersdata WHERE product_name =?',(productName,))
    data=c.fetchall()
    return data

def get_seller_product_buyernames_of_user(productName):
    c.execute('SELECT (buyersdata.username) FROM (buyersdata,sellersdata) WHERE sellersdata.product_name =? and buyersdata.product_name =?',(productName,productName))
    data=c.fetchall()
    return data

def deleteProduct_sellersdata(productName):
    c.execute("DELETE FROM sellersdata WHERE product_name =?", (productName,))
    conn.commit()

def delete_product_sellersdataUsername(productName,username):
    c.execute("DELETE FROM sellersdata WHERE product_name =? AND username=?", (productName, username))
    status = "sorry for the inconvenience. Product has been deleted"
    pending_status = "pending"
    c.execute('UPDATE buyersdata SET status =? WHERE status =? AND product_name =?',(status, pending_status, productName))
    conn.commit()

## for buyers data
def add_buyerdata(productName,bidamt,name,status):
    c.execute('INSERT INTO buyersdata(product_name,amt,username,status) VALUES (?,?,?,?)',(productName,bidamt,name,status))
    conn.commit()

def view_buyer_products_of_user(name):
    c.execute('SELECT product_name,amt,status FROM buyersdata WHERE username =?',(name,))
    data=c.fetchall()
    return data

def view_all_buyersdata():
    c.execute('SELECT * FROM buyersdata')
    data=c.fetchall()
    return data

def view_all_buyerdetails_for_productname(productname):
    c.execute('SELECT buyersdata.username,buyersdata.amt FROM (buyersdata,sellersdata) WHERE buyersdata.product_name =? AND sellersdata.product_name =?',(productname,productname))
    data=c.fetchall()
    return data

def view_bidder_amount_particularProduct(username,productname):
    c.execute('SELECT amt FROM buyersdata WHERE username=? AND product_name=?',(username,productname))
    data=c.fetchall()
    return data

def update_status_allocated_buyersdata(username,productName,amount):
    status="alloted"
    c.execute('UPDATE buyersdata SET status =? WHERE username =? AND product_name =? AND amt =?',(status,username,productName,amount))
    conn.commit()

def update_status_not_allocated_buyersdata(productName):
    status="not_alloted"
    pending_status="pending"
    c.execute('UPDATE buyersdata SET status =? WHERE status =? AND product_name =?', (status,pending_status,productName))
    conn.commit()



######## conversion data
def encode_text(text):
    encoded = text.encode()
    return encoded

def encrypt_text(key,msg_encoded):
    f = Fernet(key)
    encrypted = f.encrypt(msg_encoded)
    return encrypted

def decrypt_text(key,encrypted_msg):
    f=Fernet(key)
    decrypted=f.decrypt(encrypted_msg)
    return decrypted

def decode_orignal_text(decrypted_msg):
    orignal=decrypted_msg.decode()
    return orignal

def main():
    key = b'nNjpIl9Ax2LRtm-p6ryCRZ8lRsL0DtuY0f9JeAe2wG0='

    st.title("ONLINE AUCTION SYSTEM")
    menu=["Home","Admin Login","Seller Login","Buyer Login","SignUp"]
    choice= st.sidebar.selectbox("Menu",menu)
    if choice=="Home":
        st.subheader("Home")
        url="https://i.imgur.com/z7wDnPS.jpg"
        url_image_loader(url)
        st.markdown("#### Welcome to the Secure Online Auction System")
        sentence='<p style="font-family:sans-serif;font-size: 18px;">This is an Online Auction System,\nit is more or less same as an Offline Auction Process,\nexcept here everything is done in a secured mannered. </p>'
        st.markdown(sentence, unsafe_allow_html=True)
        st.markdown("#### INSTRUCTIONS:")
        sentence='<p style="font-family:sans-serif;font-size: 18px;">Sections in the Menu Bar.</p>'
        st.markdown(sentence, unsafe_allow_html=True)

        sentence='<p style="font-family:sans-serif;font-size: 15px;"> \n 1. Seller Login: For Logging into seller account.</p>'
        st.markdown(sentence,unsafe_allow_html=True)

        sentence = '<p style="font-family:sans-serif;font-size: 15px;"> \n 2. Buyer Login: For Logging into buyer account.</p>'
        st.markdown(sentence, unsafe_allow_html=True)

        sentence = '<p style="font-family:sans-serif;font-size: 15px;"> \n 3. SignUp: For creating a buyer/seller account.</p>'
        st.markdown(sentence, unsafe_allow_html=True)

        sentence = '<p style="font-family:sans-serif;font-size: 15px;"> \n 4. Admin Login: Only for Admin</p>'
        st.markdown(sentence, unsafe_allow_html=True)



    elif choice== "Seller Login":## seller login part
        st.subheader("Seller Login Section")
        url_image_loader("https://i.imgur.com/AfwMWt0.jpg?1")
        username=st.sidebar.text_input("User Name")
        password=st.sidebar.text_input("Password",type='password')


        if st.sidebar.checkbox("Login"):
            create_tables()
            accountType="Seller"

            result = False
            res = get_password(username, accountType)
            for i in res:
                pass_en = i[0]
                password_decrypted = decrypt_text(key, pass_en)
                password_decoded = decode_orignal_text(password_decrypted)
                if password_decoded == password:
                    result = True

            if result == True:
                st.success("Logged in as {}".format(username))
                task=st.selectbox("Task",["select the options","Add New Product","View your products","View product details","Bidder Selection","Delete Product"])
                if task =="Add New Product":
                    st.subheader("Add your Product Details here")
                    product_name=st.text_input("Enter Product Name")
                    product_minimum_price=st.text_input("Enter the minimum price to buy this product")
                    uploadFile = st.file_uploader(label="Upload image", type=['jpg', 'png', 'jpeg'])
                    if st.button("Submit"):
                        productnameList=check_product_name_based_on_productName(product_name)
                        #print(productnameList)
                        if len(productnameList)==0:
                            # Checking the Format of the page
                            if uploadFile is not None and product_name!="" and product_minimum_price!="":
                                if product_minimum_price.isdigit():
                                    img = convertToBinaryData(uploadFile)
                                    st.image(img)
                                    st.write("Image Uploaded Successfully")
                                    add_imgdata(product_name, img)
                                    add_sellersdata(product_name, product_minimum_price, username)
                                    st.success("You have created a product")
                                    st.info("Go to view your products to see ur updated products")
                                else:
                                    st.warning("amount should be in only INR(Rupees)....")
                            elif uploadFile is None and product_name!="" and product_minimum_price!="":
                                st.warning("Make sure you image is in JPG/PNG/JPEG Format and image must be uploaded.")
                            else:
                                st.warning("PRODUCT NAME and PRODUCT MINIMUM AMOUNT should not be empty and PHOTO must be uploaded.")
                        else:
                            st.warning("use a different product name...")

                elif task =="View your products":
                    st.subheader("View your products")
                    productSearch=view_all_seller_products_of_user(username)
                    #pandas_db = pd.DataFrame(productSearch, columns=["Product Name", "Minimum Product Price", "Username"])
                    #st.dataframe(pandas_db)

                    pandas_db = pd.DataFrame(productSearch,columns=["Product Name", "Minimum Product Price"])
                    st.dataframe(pandas_db)

                elif task=="View product details":
                    st.subheader("View product details")
                    Products = get_seller_products_names_of_the_user(username)
                    productsList=modification(Products)
                    ProductSelection = st.selectbox("product selection",productsList)
                    productAmt = ""
                    for i in productsList:
                        if i==ProductSelection:
                            productAmt=get_seller_product_amount_of_the_user(i)
                            break
                    lo=modification(productAmt)
                    amt=str(' '.join(lo))
                    statement = "minimum bid amount:" + amt
                    st.info(statement)
                    buyerDetails=view_all_buyerdetails_for_productname(ProductSelection)
                    pandas_db = pd.DataFrame(buyerDetails, columns=["username","product price"])
                    st.dataframe(pandas_db)
                    img_data=get_imgdata(ProductSelection)
                    for i in img_data:
                        for j in i:
                            st.image(j)
                elif task=="Bidder Selection":
                    st.subheader("Bidder Selection")
                    Products = get_seller_products_names_of_the_user(username)
                    productsList = modification(Products)
                    ProductSelection = st.selectbox("product selection", productsList)
                    bidderNames=get_seller_product_buyernames_of_user(ProductSelection)
                    bidderNamesList=modification(bidderNames)
                    #
                    bidderNamesList=set(bidderNamesList)
                    #
                    BidderSelection= st.selectbox("Select Your Bidder",bidderNamesList)
                    bidderamt=view_bidder_amount_particularProduct(BidderSelection,ProductSelection)
                    lo=modification(bidderamt)
                    #amt = str(' '.join(lo))
                    #statement="bid amount: "+amt
                    #st.info(statement)
                    bid_amount_selection=st.selectbox("Select Bid amount",lo)
                    if st.button("Allocate"):
                        #if BidderSelection is not None and ProductSelection is not None and len(amt)!=0:
                        if BidderSelection is not None and ProductSelection is not None and bid_amount_selection is not None:
                            update_status_allocated_buyersdata(BidderSelection,ProductSelection,bid_amount_selection)
                            update_status_not_allocated_buyersdata(ProductSelection)
                            deleteProduct_sellersdata(ProductSelection)
                            delete_imgdata_productname(ProductSelection)
                            st.info("allocation done sucessfully.....")
                        else:
                            st.warning("bidder/product/bid_amount should not be empty.")
                elif task=="Delete Product":
                    st.subheader("Delete Product")
                    Products = get_seller_products_names_of_the_user(username)
                    productsList = modification(Products)
                    ProductSelection = st.selectbox("product selection", productsList)
                    if st.button("Delete Product"):
                        delete_product_sellersdataUsername(ProductSelection,username)
                        st.success("Sucessfully Prodyct has been deleted")



            else:
                st.warning("Incorrect Username/password")
    elif choice== "Buyer Login":## buyer login part
        st.subheader("Buyer Login Section")
        url_image_loader("https://i.imgur.com/WiNza3c.jpg?1")
        username=st.sidebar.text_input("User Name")
        password=st.sidebar.text_input("Password",type='password')


        if st.sidebar.checkbox("Login"):
            create_tables()
            accountType="Buyer"
            result = False
            res = get_password(username, accountType)
            for i in res:
                pass_en = i[0]
                password_decrypted = decrypt_text(key, pass_en)
                password_decoded = decode_orignal_text(password_decrypted)
                if password_decoded == password:
                    result = True

            if result == True:
                st.success("Logged in as {}".format(username))
                task=st.selectbox("Task",["select the options","Apply For a Product","View All Available Products","View Your Bids"])
                if task =="Apply For a Product":
                    st.subheader("Enter the required details for applying for that auction")
                    productList=view_all_productnames_sellerdata()
                    product_name=modification(productList)
                    ProductSelection = st.selectbox("product selection", product_name)
                    # img viewing
                    img_data = get_imgdata(ProductSelection)
                    for i in img_data:
                        for j in i:
                            st.image(j)

                    productAmt = get_seller_product_amount_of_the_user(ProductSelection)
                    lo = modification(productAmt)
                    amt = str(' '.join(lo))
                    statement = "minimum bid amount: " + amt
                    st.info(statement)
                    product_price=st.text_input("Enter the amount to purchase the product")
                    proposedAmount=get_seller_product_amount_of_the_user(ProductSelection)
                    lo = modification(proposedAmount)

                    amt = str(' '.join(lo))

                    if st.button("Submit"):
                        if product_price=="":
                            st.warning("amount should not be empty")
                        if product_price!="":
                            if product_price.isdigit():
                                if int(amt)<int(product_price):
                                    status = "pending"
                                    add_buyerdata(ProductSelection, product_price, username, status)
                                    st.success("sucessfully your bid has been placed.")
                                    st.info("Go to view your bids to see ur updated products")
                                else:
                                    st.warning("your bid amount should be more than the amount proposed")
                            else:
                                st.warning("your bid amount should be only in INR(Rupees)")

                elif task=="View All Available Products":
                    st.subheader("Products Available For Auction")
                    allProducts=view_all_sellersdata()
                    pandas_db=pd.DataFrame(allProducts,columns=["Product Name","Product Price","Seller Username"])
                    st.dataframe(pandas_db)

                elif task=="View Your Bids":
                    st.subheader("View your bids")
                    productSearch = view_buyer_products_of_user(username)
                    pandas_db = pd.DataFrame(productSearch, columns=["Product Name", "Your Bidding Price","Status"])
                    st.dataframe(pandas_db)

            else:
                st.warning("Incorrect Username/password")

    elif choice== "Admin Login":
        st.subheader("Admin Login Section")
        url_image_loader("https://i.imgur.com/xxTUknZ.png?1")
        username=st.sidebar.text_input("User Name")
        password=st.sidebar.text_input("Password",type='password')

        #####
        create_tables()
        usernameList = view_user("admin")
        if len(usernameList) == 0:
            p = "Rvhk7!_E34QMJqhg"
            p_encode = encode_text(p)
            p_en = encrypt_text(key, p_encode)
            add_userdata("admin", p_en, "admin")
        #####

        if st.sidebar.checkbox("Login"):
            create_tables()
            accountType = "admin"
            result=False
            res=get_password(username,accountType)
            for i in res:
                pass_en=i[0]
                password_decrypted=decrypt_text(key,pass_en)
                password_decoded=decode_orignal_text(password_decrypted)
                if password_decoded==password:
                    result=True

            if result==True:
                st.success("Logged in as {}".format(username))

                task=st.selectbox("Task",["All Auctions","All Buyers","Profiles","img data","Reset All"])
                if task =="All Auctions":
                    st.subheader("Auctions")
                    if username=="admin" and password=="Rvhk7!_E34QMJqhg":
                        user_result=view_all_sellersdata()
                        #printing the database in the form of the pandas dataframe
                        pandas_db=pd.DataFrame(user_result,columns=["Product Names","Minimum Product Amount","Seller Username"])
                        st.dataframe(pandas_db)
                    else:
                        st.warning("only Admin Dept can access this ....")

                elif task =="All Buyers":
                    st.subheader("Buyers")
                    if username=="admin" and password=="Rvhk7!_E34QMJqhg":
                        user_result=view_all_buyersdata()
                        #printing the database in the form of the pandas dataframe
                        pandas_db=pd.DataFrame(user_result,columns=["Product Names"," Bid Amounts","Bidder Usernames","Status"])
                        st.dataframe(pandas_db)
                    else:
                        st.warning("only Admin Dept can access this ....")

                elif task =="Profiles":
                    if username=="admin" and password=="Rvhk7!_E34QMJqhg":
                        st.subheader("User Profiles")
                        user_result=view_all_usersdata()


                        #####for showing data after decryption
                        #user_re = convert_data_to_string_format_list(key, user_result)
                        #pandas_db=pd.DataFrame(user_re,columns=["Username","Password","accountType"])
                        # st.dataframe(pandas_db)
                        #######

                        # printing the database in the form of the pandas dataframe
                        db2=pd.DataFrame(user_result,columns=["Username","Password","Account Type"])
                        st.dataframe(db2)
                    else:
                        st.warning("only Admin Dept can access this ....")
                elif task=="img data":
                    if username=="admin" and password=="Rvhk7!_E34QMJqhg":
                        st.subheader("Image dataset")
                        productnames=get_productNames_imgdata()
                        productnamesList=modification(productnames)
                        ProductSelection=st.selectbox("Product Selection",productnamesList)
                        img_data = get_imgdata(ProductSelection)
                        for i in img_data:
                            for j in i:
                                st.image(j)
                    else:
                        st.warning("only Admin Dept can access....")
                elif task=="Reset All":
                    if username=="admin" and password=="Rvhk7!_E34QMJqhg":
                        p=st.text_input("Enter Password:",type='password')
                        if st.button("Submit"):
                            if p=="Rvhk7!_E34QMJqhg":
                                drop_all_tables()
                            else:
                                st.warning("only Admin Dept can access....")
                    else:
                        st.warning("only Admin Dept can access....")
            else:
                st.warning("Incorrect Username/password")

    elif choice=="SignUp":
        st.subheader("Create New Account")
        new_user=st.text_input("User Name")
        new_password=st.text_input("Password",type='password')

        account_type_choice=st.selectbox("Account Type",["Seller","Buyer"])
        if account_type_choice=="Seller":
            account_type="Seller"

        elif account_type_choice=="Buyer":
            account_type="Buyer"
        if st.button("SignUp"):
            if new_user=="" or new_password=="":
                st.warning("Username or Password should not be empty..")

            elif new_user!="" or new_password!="":
                create_tables()
                userList=view_user(new_user)
                if len(userList)==0:
                    #create_tables()
                    new_password=encode_text(new_password)
                    new_password=encrypt_text(key,new_password)
                    add_userdata(new_user, new_password, account_type)
                    st.success("You have created an account")
                    st.info("Go to Login to login")
                else:
                    st.warning("Username has been created please use other username.....")
        st.markdown(" ### Account Type:")
        st.markdown("####   1. Seller Account:")
        sentence = '<p style="font-family:sans-serif;font-size: 20px;">It is a type of account where you can publish your products along with the \nminimum bidding price and buyers can bid for them, allocate the Product to \na Buyer whose Bidding Price you are satisfied with.</p>'
        st.markdown(sentence, unsafe_allow_html=True)
        #st.text("It is a type of account where you can publish your products along with the \nminimum bidding price and buyers can bid for them, allocate the Product to \na Buyer whose Bidding Price you are satisfied with.")
        st.markdown("####   2. Buyer Account:")
        sentence = '<p style="font-family:sans-serif;font-size: 20px;">It is a type of account where you can see the available products along with their \nbidding price, if you like to buy a product you have to bid for an amount which is \ngreater than the minimum bidding price.</p>'
        st.markdown(sentence, unsafe_allow_html=True)
        #st.text("It is a type of account where you can see the available products along with their \nbidding price, if you like to buy a product you have to bid for an amount which is \ngreater than the minimum bidding price.")


if __name__=='__main__':
    main()
