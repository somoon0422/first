def paginate_search_results(results, page_size, page_number):
    start = (page_number - 1) * page_size
    end = start + page_size
    return results[start:end]

# Example usage:
results = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
page_size = 3
for page_number in range(1, 4):
    print(f"Page {page_number}: {paginate_search_results(results, page_size, page_number)}")
