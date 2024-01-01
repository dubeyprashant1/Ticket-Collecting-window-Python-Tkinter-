from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from register import *

def main():
    root=Tk()
    app=login_class(root)
    root.mainloop()

class login_class:
    def __init__(self, win):
        self.win = win
        self.win.title("Login")
        self.win.geometry("1550x800+0+0")
        
        self.load_bg_image()
        self.load_loginframe()
        self.sentence="Welcome to Railway Ticket Window"
        self.current_index=0
        self.update1_label()
        
    def update1_label(self):
        current_letter = self.sentence[self.current_index]
        self.heading_label.config(text=self.heading_label.cget("text") + current_letter)
        self.current_index += 1
        
        if self.current_index >= len(self.sentence):
            current_index = 0
            # Pause for 3 seconds when the entire string is displayed
            self.win.after(500, self.clear_label)
        else:
            self.win.after(50, self.update1_label)  # Schedule the update after 100 milliseconds (0.1 second)

    # Function to clear the label text
    def clear_label(self):
        self.heading_label.config(text="")
        self.update1_label()
        
    def load_bg_image(self):
        original_image = Image.open("login_bg0.jpg")
        resized_image = original_image.resize((1650,900))
        self.bg = ImageTk.PhotoImage(resized_image)
        
        loginbg0_lbl = Label(self.win, image=self.bg)
        loginbg0_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        heading_label = Label(self.win, text="",font=("times new roman",40,"bold"),fg="green",highlightbackground="black",highlightthickness=4)
        heading_label.place(x=250, y=50)
        
    def load_loginframe(self):    
        loginframe0=Frame(self.win,bg="black")    
        loginframe0.place(x=510,y=170,width=340,height=450)
        
        img1=Image.open("framelogin0.png")
        img1=img1.resize((100,100))
        self.frameimg1=ImageTk.PhotoImage(img1)
        frameimg_lbl=Label(image=self.frameimg1,bg="black",borderwidth=1)
        frameimg_lbl.place(x=630,y=180,width=100,height=100)

        getstart_lbl=Label(loginframe0,text="Get Started",font="verdana 20 bold",fg="white",bg="black")
        getstart_lbl.place(x=90,y=110)
        
        #labels entries
        username_lbl=Label(loginframe0,text="Username",font=("times new roman",15,"bold"),fg="white",bg="black")
        username_lbl.place(x=70,y=165)
        self.username_txt=ttk.Entry(loginframe0,font=("times new roman",15,"bold"))
        self.username_txt.place(x=40,y=192,width=270)
        
        password_lbl=Label(loginframe0,text="Password",font=("times new roman",15,"bold"),fg="white",bg="black")
        password_lbl.place(x=70,y=235)
        self.password_txt=ttk.Entry(loginframe0,font=("times new roman",15,"bold"))
        self.password_txt.place(x=40,y=267,width=270)
        
        #icon images
        icon_img1=Image.open("usernameicon.png")
        icon_img1=icon_img1.resize((25,25))
        self.icon1=ImageTk.PhotoImage(icon_img1)
        frameimg_lbl=Label(loginframe0,image=self.icon1,bg="black",borderwidth=1)
        frameimg_lbl.place(x=40,y=165,width=25,height=25)
        
        icon_img2=Image.open("passwordicon.png")
        icon_img2=icon_img2.resize((25,25))
        self.icon2=ImageTk.PhotoImage(icon_img2)
        frameimg_lbl=Label(loginframe0,image=self.icon2,bg="black",borderwidth=1)
        frameimg_lbl.place(x=40,y=235,width=25,height=25)
        
        #login button
        login_btn=Button(loginframe0,command=self.login_validation,text="Login", font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="red",activeforeground="white",activebackground="red")
        login_btn.place(x=110,y=310,width=120,height=35)
        
        #register new user button
        login_btn=Button(loginframe0,command=self.register_window,text="New User Register", font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        login_btn.place(x=20,y=370,width=160)
        
        #forgot password button
        login_btn=Button(loginframe0,command=self.forgot_pass, text="Forget Password?", font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        login_btn.place(x=18,y=390,width=160)
    
    def register_window(self):
        self.new_window=Toplevel(self.win)
        self.app=register_class(self.new_window)
        
    def login_validation(self):
        if self.username_txt.get()==""or self.password_txt.get()=="":
            messagebox.showerror("Error","All Field are Required")
        elif self.username_txt.get()=="prashant" and self.password_txt.get()=="12345":
            messagebox.showinfo("Success","Welcome to Ticket Booking Platform")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="123456",database="passengerregister")
            my_cursor=conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s",(
                self.username_txt.get(),
                self.password_txt.get()
            ))
            row=my_cursor.fetchone()
            if(row==None):
                messagebox.showerror("Error","Invalid Username and Password")
            else:
                open_main=messagebox.askyesno("YesNo","Access only admins")
                if open_main>0:
                    self.new_window=Toplevel(self.win)
                    self.app=register_class(self.new_window)           
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()
            
            
    def reset_pass(self):
        if self.comboques.get()=="Select":
            messagebox.showerror("Error","Select the security question",parent=self.root2)
        elif self.securityans_entry.get()=="":
            messagebox.showerror("Error","Please enter the security Answer",parent=self.root2)
        elif self.new_pass_entry.get()=="":
            messagebox.showerror("Error","Please enter the New password",parent=self.root2)
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="123456",database="passengerregister")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s and Securityques=%s and securityans=%s")
            value=(self.username_txt.get(),self.comboques.get(),self.securityans_entry.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Please Enter Correct Answer",parent=self.root2)
            else:
                query=("update register set password=%s where email=%s")
                value=(self.new_pass_entry.get(),self.username_txt.get(),)
                my_cursor.execute(query,value)
                
                conn.commit()
                conn.close()
                messagebox.showinfo("Updated","Your Password has been updated Successfully",parent=self.win)
                self.root2.destroy()
            
    
    
    
    def forgot_pass(self):
        if self.username_txt.get()=="":
            messagebox.showerror("Error","Please enter the email address to reset password")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="123456",database="passengerregister")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.username_txt.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            
            if(row==None):
                messagebox.showerror("Error","Please enter the valid user name")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.configure(bg="white")
                self.root2.geometry("360x450+500+180")
                
                l1=Label(self.root2,text="Forget Password", font=("times new roman",20,"bold"),fg="red",bg="white")
                l1.place(x=0,y=10,relwidth=1)
                securityques_lbl=Label(self.root2,text="Select Security Questions",font=("times new roman",15,"bold"),fg="black",bg="white")
                securityques_lbl.place(x=50,y=80)
                self.comboques=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.comboques["values"]=("Select","Your Birth Place","Your First School","Your Nick Name","Your Pet Name","Your Friend Name")
                self.comboques.place(x=50,y=110,width=250)
                self.comboques.current(0)

                securityans_lbl=Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),fg="black",bg="white")
                securityans_lbl.place(x=50,y=150)
                self.securityans_entry=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.securityans_entry.place(x=50,y=180,width=250)
                
                new_pass=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),fg="black",bg="white")
                new_pass.place(x=50,y=220)
                self.new_pass_entry=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.new_pass_entry.place(x=50,y=250,width=250)

                btn1=Button(self.root2,text="Reset",command=self.reset_pass,font=("times new roman",15,"bold"),fg="white",bg="green",border="1px solid black",activebackground="green",activeforeground="white")
                btn1.place(x=150,y=29)
                
            
        
class register_class:
    def __init__(self,win):
        self.win=win
        self.win.title("Register")
        self.win.geometry("1650x900+0+0")
        self.load_bg_image()
        self.load_registerframe()

    def load_bg_image(self):
        original_image = Image.open("register_bg0.webp")
        resized_image = original_image.resize((1650,900))
        self.bg = ImageTk.PhotoImage(resized_image)
        
        loginbg0_lbl = Label(self.win, image=self.bg)
        loginbg0_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        loginbg0_lbl2 = Label(self.win, text="Register New User",font=("times new roman",50,"bold"),fg="blue",highlightbackground="black",highlightthickness=4)
        loginbg0_lbl2.place(x=350, y=50)
        
    def load_registerframe(self):    
        registerframe0=Frame(self.win,bg="black",border="4px solid")   
        registerframe0.place(x=100,y=170,width=1100,height=470)    
        
        img1=Image.open("formbg_leftimg.png")
        img1=img1.resize((500,450))
        self.frameimg1=ImageTk.PhotoImage(img1)
        frameimg_lbl=Label(registerframe0, image=self.frameimg1,bg="black",borderwidth=1)
        frameimg_lbl.place(x=0,y=0,width=450,height=460)
        
        register_lbl=Label(registerframe0,text="REGISTER HERE",font=("verdana",25,"bold"),fg="yellow",bg="black")
        register_lbl.place(x=470,y=20)
        
        #labels and entries
        
        # creating Variables
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityQ=StringVar()
        self.var_securityA=StringVar()
        self.var_pass=StringVar()
        self.var_confpass=StringVar()
        self.var_check=IntVar()
        
        #row1
        fname_lbl=Label(registerframe0,text="First Name",font=("times new roman",15,"bold"),bg="black",fg="white")
        fname_lbl.place(x=500,y=80)
        self.fname_entry=ttk.Entry(registerframe0,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        self.fname_entry.place(x=500,y=110,width=250)

        lname_lbl=Label(registerframe0,text="Last Name",font=("times new roman",15,"bold"),bg="black",fg="white")
        lname_lbl.place(x=820,y=80)
        self.lname_entry=ttk.Entry(registerframe0,textvariable=self.var_lname,font=("times new roman",15,"bold"))
        self.lname_entry.place(x=820,y=110,width=250)
        
        #row 2
        contact_lbl=Label(registerframe0,text="Contact No.",font=("times new roman",15,"bold"),bg="black",fg="white")
        contact_lbl.place(x=500,y=150)
        self.contact_entry=ttk.Entry(registerframe0,textvariable=self.var_contact,font=("times new roman",15,"bold"))
        self.contact_entry.place(x=500,y=180,width=250)
        
        email_lbl=Label(registerframe0,text="E-Mail",font=("times new roman",15,"bold"),bg="black",fg="white")
        email_lbl.place(x=820,y=150)
        self.email_entry=ttk.Entry(registerframe0,textvariable=self.var_email,font=("times new roman",15,"bold"))
        self.email_entry.place(x=820,y=180,width=250)
        
        #row3
        securityques_lbl=Label(registerframe0,text="Select Security Questions",font=("times new roman",15,"bold"),bg="black",fg="white")
        securityques_lbl.place(x=500,y=220)
        self.comboques=ttk.Combobox(registerframe0,textvariable=self.var_securityQ,font=("times new roman",15,"bold"),state="readonly")
        self.comboques["values"]=("Select","Your Birth Place","Your First School","Your Nick Name","Your Pet Name","Your Friend Name")
        self.comboques.place(x=500,y=250,width=250)
        self.comboques.current(0)

        securityans_lbl=Label(registerframe0,text="Security Answer",font=("times new roman",15,"bold"),bg="black",fg="white")
        securityans_lbl.place(x=820,y=220)
        self.securityans_entry=ttk.Entry(registerframe0,textvariable=self.var_securityA,font=("times new roman",15,"bold"))
        self.securityans_entry.place(x=820,y=250,width=250)
        
        #row4
        password_lbl=Label(registerframe0,text="Password",font=("times new roman",15,"bold"),bg="black",fg="white")
        password_lbl.place(x=500,y=290)
        self.password_entry=ttk.Entry(registerframe0,textvariable=self.var_pass,font=("times new roman",15,"bold"))
        self.password_entry.place(x=500,y=320,width=250)
        
        confirmpassword_lbl=Label(registerframe0,text="Confirm Password",font=("times new roman",15,"bold"),bg="black",fg="white")
        confirmpassword_lbl.place(x=820,y=290)
        self.confirmpassword_entry=ttk.Entry(registerframe0,textvariable=self.var_confpass,font=("times new roman",15,"bold"))
        self.confirmpassword_entry.place(x=820,y=320,width=250)
        
        #checkbutton
        checkbtn=Checkbutton(registerframe0,variable=self.var_check,text="I Agree The Terms & Conditions",font=("times new roman",13,"bold"),onvalue=1,offvalue=0,bg="white",activebackground="white",activeforeground="black")
        checkbtn.place(x=500,y=360)
        
        # buttons
        register_img0=Image.open("registerbtnimg.png")
        register_img0=register_img0.resize((150,50))
        self.register_btnimg=ImageTk.PhotoImage(register_img0)
        reg_btn1=Button(registerframe0,command=self.register_validation,image=self.register_btnimg,borderwidth=0,cursor="hand2",bg="black",activebackground="black")
        reg_btn1.place(x=600,y=400,width=150,height=50)

        loginagain_img=Image.open("loginnowbtn.jpg")
        loginagain_img=loginagain_img.resize((150,40))
        self.loginagain_btnimg=ImageTk.PhotoImage(loginagain_img)
        loginagain_btn2=Button(registerframe0,command=self.return_login,image=self.loginagain_btnimg,borderwidth=0,cursor="hand2",bg="black",activebackground="black")
        loginagain_btn2.place(x=850,y=400,width=150,height=50)
        
    def register_validation(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityQ.get()=="":
            messagebox.showerror("Error","All Fields are Required",parent=self.win)
        elif self.var_pass.get()!=self.var_confpass.get():    
            messagebox.showerror("Error","Password and Confirm Password must be same",parent=self.win)
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Please Agree the Terms & Conditions",parent=self.win)
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="123456",database="passengerregister")
            my_cursor=conn.cursor()
            query=("Select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if(row!=None):
                messagebox.showerror("Error","User Already Exist, Please try another Email",parent=self.win)
            else:
                my_cursor.execute("Insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                    self.var_fname.get(),
                    self.var_lname.get(),
                    self.var_contact.get(),
                    self.var_email.get(),
                    self.var_securityQ.get(),
                    self.var_securityA.get(),
                    self.var_pass.get()
                ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Registered Successfully",parent=self.win)
            self.win.destroy()
            
    def return_login(self):
        self.win.destroy()
        
if __name__ == "__main__":
    main()
    
