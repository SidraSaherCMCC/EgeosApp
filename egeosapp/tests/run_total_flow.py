# Import the TotalFlow class
from total_flow import TotalFlow

def main():
    # Create an instance of the TotalFlow class
    total_flow_instance = TotalFlow()

    # Set your file ID and other parameters
    file_id = "CSKS1_DGM_B_WR_00_VV_RA_FF_20210607042748_20210607042803_2021-0"

    try:
        # Run the total flow
        result = total_flow_instance.run_total_flow(file_id)

        # Print the result
        print(result)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Run the main function
    main()
