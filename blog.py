class Blog:
    def __init__(self):
        self.users = set()
        self.posts = []
        self.current_user = None  # attribute used to determine if there is a logged in user

    # Private method for getting a post instance from the blog based on its ID
        # returns None if post with ID does not exist
    def _get_post_from_id(self, post_id):
        for post in self.posts:
            if post.id == int(post_id):
                return post

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
        # get user credentials
        username = input("What is your username? ")
        password = input("What is your password? ")
        # loop through each user in the blog
        for user in self.users:
            if user.username == username and user.check_password(password):
                # if user has correct credentials, set the blog's current user to that user instance
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

    # Method to create a new post if the user is logged in
    def create_post(self):
        # Check to make sure the user is logged in before creating a post
        if self.current_user is not None:
            # Get the title and body from user input
            title = input("Enter the title of your post: ")
            body = input("Enter the body of your post: ")
            # Create new Post instance with the given input
            new_post = Post(title, body, self.current_user)
            # Add the new post instance to our blog's list of posts
            self.posts.append(new_post)
            print(f"{new_post.title} has been created!")
        else:
            print("You must be logged in to perform this action.")

    # Method to view blog posts
    def view_posts(self):
        # Check to see if there are any posts
        if self.posts:
            # Loop through all the posts
            for post in self.posts:
                # Display the post
                print(post)
        # If no posts
        else:
            print("There are currently no posts for this blog :( ")

    # Method to view a SINGLE post by ID
    def view_post(self, post_id):
        #
        post = self._get_post_from_id(post_id)
        if post:
            print(post)
        else:
            print(f"Post with the ID of {post_id} does not exist.")

    # Method to edit a post by ID
    def edit_post(self, post_id):
        post = self._get_post_from_id(post_id)
        if post:
            # Check that the user is logged in and the logged in user is the author of the post
            if self.current_user is not None and self.current_user == post.author:
                print(post)
                # Ask the user which part of the post they would like to edit
                edit_part = input(
                    "Would you like to edit the title, body, both, or exit? ")
                while edit_part not in {'title', 'body', 'both', 'exit'}:
                    edit_part = input(
                        "Invalid Option. Title, Body, Both, or Exit? ")
                # if the user types exit; exit the function
                if edit_part == 'exit':
                    return
                elif edit_part == 'both':
                    # Get new title and body
                    new_title = input("Enter the new title: ")
                    new_body = input("Enter the new body: ")
                    # edit the post with the post.update method
                    post.update(title=new_title, body=new_body)
                elif edit_part == 'title':
                    new_title = input("Enter the new title: ")
                    post.update(title=new_title)
                elif edit_part == 'body':
                    new_body = input("Enter the new body: ")
                    post.update(body=new_body)
                print(f"{post.title} has been updated!")
            # If the user is logged in BUT not the author of the post
            elif self.current_user is not None and self.current_user != post.author:
                # 403 HTTP status code
                print("You do not have permission to edit this post.")
            # If the user is not logged in
            else:
                # 401 HTTP status code
                print("You must be logged in to perform this action.")
        else:
            # 404 HTTP status code
            print(f"Post with the ID of {post_id} does not exist.")

    # Method to delete a post by its ID
    def delete_post(self, post_id):
        post = self._get_post_from_id(post_id)
        if post:
            # Check that the user is logged in and the logged in user is the author of the post
            if self.current_user is not None and self.current_user == post.author:
                self.posts.remove(post)
                print(f"{post.title} has been removed!")
            # If the user is logged in BUT not the author of the post
            elif self.current_user is not None and self.current_user != post.author:
                # 403 HTTP status code
                print("You do not have permission to delete this post.")
            # If the user is not logged in
            else:
                # 401 HTTP status code
                print("You must be logged in to perform this action.")
        else:
            # 404 HTTP status code
            print(f"Post with the ID of {post_id} does not exist.")


class User:
    id_counter = 1  # class attribute keeping track of User IDs

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
    id_counter = 1

    def __init__(self, title, body, author):
        """
        title: str
        body: str
        author: user
        """
        self.title = title
        self.body = body
        self.author = author
        self.id = Post.id_counter
        Post.id_counter += 1

    def __str__(self):
        formatted_post = f"""
        {self.id} - {self.title.title()}
        By: {self.author}
        {self.body}
        """
        return formatted_post

    def __repr__(self):
        return f"<Post {self.id}|{self.title}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# define a function to run the blog
def run_blog():
    # Create an instance of the Blog Class
    my_blog = Blog()
    # Add pre-loaded data for the blog
    initial_user = User('brians', 'abc123')
    my_blog.users.add(initial_user)
    initial_post = Post('Pre-Loaded', 'This post was preloaded', initial_user)
    my_blog.posts.append(initial_post)

    # Keep looping while the blog is "running"
    while True:
        # if there is no current user logged in
        if my_blog.current_user is None:
            # Print the menu option
            print(
                "1. Sign Up \n2. Log In\n3. View All Posts\n4. View Single Post\n5. Quit")
            # Ask the user which option they would like to do
            to_do = input('Which option would you like to do? ')
            # Keep asking if user chooses an invalid option
            while to_do not in {'1', '2', '3', '4', '5'}:
                to_do = input(
                    'Invalid option. Please choose 1, 2, 3, 4 or 5. ')
            if to_do == '5':
                print('Thanks for checking out the blog!')
                break
            elif to_do == '1':
                # method to create new user
                my_blog.create_new_user()
            elif to_do == '2':
                # method to log user in
                my_blog.log_user_in()
            elif to_do == '3':
                # method to view all posts
                my_blog.view_posts()
            elif to_do == '4':
                # get the id of the post
                post_id = input(
                    "What is the ID of the post you would like to view? ")
                # Call the 'view single post' method with the post_id as an argument
                my_blog.view_post(post_id)

        # If the current user is not None aka a user is logged in
        else:
            # Print menu options for logged in user
            print("1. Log Out\n2. Create New Post\n3. View All Posts\n4. View Single Post\n5. Edit A Post\n6. Delete A Post")
            to_do = input("Which option would you like to choose? ")
            while to_do not in {'1', '2', '3', '4', '5', '6'}:
                to_do = input(
                    "Invalid option. Please choose 1, 2, 3, 4, 5, or 6.")
            if to_do == '1':
                my_blog.log_user_out()
            elif to_do == '2':
                my_blog.create_post()
            elif to_do == '3':
                my_blog.view_posts()
            elif to_do == '4':
                # get the id of the post
                post_id = input(
                    "What is the ID of the post you would like to view? ")
                # Call the 'view single post' method with the post_id as an argument
                my_blog.view_post(post_id)
            elif to_do == '5':
                # get the id of the post we would like to edit
                post_id = input(
                    "What is the ID of the post you would like to edit? ")
                # Call the edit single post method with post_id as an argument
                my_blog.edit_post(post_id)
            elif to_do == '6':
                # Get the ID of the post we would like to delete
                post_id = input(
                    "What is the ID of the post you would like to delete? ")
                # call the delete post method with the post id as an argument
                my_blog.delete_post(post_id)


# Execute the run_blog function to run the blog
run_blog()
