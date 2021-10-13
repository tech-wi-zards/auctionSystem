import streamlit as st
import sqlite3
import pandas as pd


#database management
conn= sqlite3.connect('data.db')
c=conn.cursor()
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data= c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data=c.fetchall()
    return data





def main():

    st.title("ONLINE AUCTION SYSTEM")
    menu=["Home","Login","SignUp"]
    choice= st.sidebar.selectbox("Menu",menu)
    if choice=="Home":
        st.subheader("Home")

    elif choice== "Login":
        st.subheader("Login Section")
        username=st.sidebar.text_input("User Name")
        password=st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            #if password =="admin" and username=="admin":
            create_usertable()
            result=login_user(username,password)
            if result:
                st.success("Logged in as {}".format(username))

                task=st.selectbox("Task",["Add Post","Analytics","Profiles"])
                if task =="Add Post":
                    st.subheader("Add Your Post")

                elif task =="Analytics":
                    st.subheader("Analytics")

                elif task =="Profiles":
                    if username=="admin" and password=="admin":
                        st.subheader("User Profiles")
                        user_result=view_all_users()
                        #printing the database in the form of the pandas dataframe
                        pandas_db=pd.DataFrame(user_result,columns=["Username","Password"])
                        st.dataframe(pandas_db)
                    else:
                        st.warning("only Admin Dept can access to this sorry for the inconvince....")
            else:
                st.warning("Incorrect Username/password")


    elif choice=="SignUp":
        st.subheader("Create New Account")
        new_user=st.text_input("User Name")
        new_password=st.text_input("Password",type='password')
        if st.button("SignUp"):
            create_usertable()
            add_userdata(new_user,new_password)
            st.success("You have created an account")
            st.info("Go to Login to login")


if __name__=='__main__':
    main()