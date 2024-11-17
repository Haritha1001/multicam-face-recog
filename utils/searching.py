def binary_search(arr, element):
    start, end = 0, len(arr) - 1
    while start <= end:
        mid = (start + end) // 2
        if arr[mid] == element:
            return True
        elif element < arr[mid]:
            end = mid - 1
        else:
            start = mid + 1
    return False
