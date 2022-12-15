class Blog:
    def __init__(self):
        self.users = set()
        self.posts = []
        self.current_user = None # attribute used to determine if there is a logged in user

    # Method to add new user to the blog
    def create_new_user(self):
        # Get user info from input
        username = input('Please enter a username: ')
        # Check if username already exists
        if username in {u.username for u in self.users}:
            print(f"User with username {username} already exists")
        else:
            # Get Password
            password = input('Please enter a password: ')
            # Create a new User instanve with info from inputs
            new_user = User(username, password)
            # Add the new user instance to the blog user set
            self.users.add(new_user)
            print(f"{new_user} has been created.")

    # Method to log user in
    def log_user_in(self):
        #get user credentials
        username = input("What is your username? ")
        password = input("What is your password? ")
        #loop through each user in the blog
        for user in self.users:
            if user.username == username and user.check_password(password):
                #if user has correct credentials, set the blog's current user to that user instance
                self.current_user = user
                print(f"{user} has been logged in")
                break
        # If no users in out blog user set have that username/password, alert invalid credentials
        else:
            print("Username and/or Password is incorrect.")

    # Method to log a user out
    def log_user_out(self):
        # Change the current_user attribute on this instance to None
        self.current_user = None
        print("You have successfully logged out.")



class User:
    id_counter = 1 # class attribute keeping track of User IDs
    def __init__(self, username, password):
        self.username = username
        self.password = password[::-2]
        self.id = User.id_counter
        User.id_counter += 1

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User {self.id}|{self.username}>"

    def check_password(self, password_guess):
        return self.password == password_guess[::-2]

class Post:
    pass



#define a function to run the blog
def run_blog():
    #Create an instance of the Blog Class
    my_blog = Blog()
    #Keep looping while the blog is "running"
    while True:
        # if there is no current user logged in
        if my_blog.current_user is None:
            #Print the menu option
            print("1. Sign Up \n2. Log In\n5. Quit")
            #Ask the user which option they would like to do
            to_do = input('Which option would you like to do? ')
            #Keep asking if user chooses an invalid option
            while to_do not in {'1','2','5'}:
                to_do = input('Invalid option. Please choose 1, 2, or 5. ')
            if to_do == '5':
                print('Thanks for checking out the blog!')
                break
            elif to_do == '1':
                #method to create new user
                my_blog.create_new_user()
            elif to_do == '2':
                # method to log user in
                my_blog.log_user_in()
        # If the current user is not None aka a user is logged in
        else:
            # Print menu options for logged in user
            print("1. Log Out")
            to_do = input("Which option would you like to choose? ")
            while to_do not in {'1'}:
                to_do = input("Invalid option. Please choose 1.")
            if to_do == '1':
                my_blog.log_user_out()
                





# Execute the run_blog function to run the blog
run_blog()