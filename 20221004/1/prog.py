el, arr = eval(input())

def f(arr, el):
    print(arr)
    if len(arr) == 1 and arr[0] != el:
        return False
    if arr[len(arr) // 2] == el:
        return True
    if arr[len(arr) // 2] < el:
        return f(arr[len(arr) // 2:], el)
    if arr[len(arr) // 2] > el:
        return f(arr[:len(arr)//2], el)
    
print(f(arr,el))
