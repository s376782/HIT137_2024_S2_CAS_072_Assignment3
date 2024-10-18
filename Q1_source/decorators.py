#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q1_source
import time

def timing(func):
    """
    Decorator to measure the execution time of a function.

    Returns:
        function: A wrapper function that executes the original function 
                  and prints its execution time.
    """    
    def wrapper(*args, **kwargs):
        # Record the start time right before the function call
        start_time = time.time()

        # Execute the original function and store the result
        result = func(*args, **kwargs)

        # Record the end time immediately after the function finishes
        end_time = time.time()

        # Calculate the elapsed time by subtracting start_time from end_time
        execution_time = end_time - start_time
        
        # Print the name of the function and its execution time, formatted to 4 decimal places
        print(f"Function {func.__name__} executed in {execution_time:.4f} seconds.")
        
        # Return the result of the original function so that the behavior remains the same
        return result

    # Return the wrapper function so that it replaces the original function with the decorated one
    return wrapper

def authorized(func):
    """
    Decorator to check if the user is authenticated using the Application singleton.
    
    Returns:
        function: A wrapper function that checks if the user is authenticated before proceeding.
    """
    def wrapper(*args, **kwargs):
        # Access the Application singleton instance

        from application import Application
        app_instance = Application()

        # Check if the user is authenticated
        if app_instance.is_user_authenticated():
            # If the user is authenticated, proceed with the original function
            return func(*args, **kwargs)
        else:
            # If the user is not authenticated, deny access
            print("Access denied. User is not authenticated.")
            return None  # Optionally return an error message or redirect

    return wrapper
