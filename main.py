import pandas as pd

# Open the text file for reading
with open('domains.csv', 'r', encoding='utf-8') as file:
    # Iterate over each line in the file
    cnt = 0
    for line in file:
        # Print the current line to the console
        # print(line.strip())  # .strip() removes the newline character at the end
        url = 'https://www.tagungshotel.com/home.php?Kundenid=' + line.strip()
        cnt += 1

df.to_excel('result.xlsx', index=False)
