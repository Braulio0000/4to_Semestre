#include <bits/stdc++.h>
using namespace std;

// A recursive binary search function. It returns
// location of x in given array arr[low..high] is present,
// otherwise -1
int binarySearch(string arr[], int low, int high, string x) {
    if (high >= low) {
        int mid = low + (high - low) / 2;
        // If the element is present at the middle itself
        if (arr[mid] == x)
            return mid;
        // If element is smaller than mid, then
        // it can only be present in left subarray
        if (arr[mid] > x)
            return binarySearch(arr, low, mid - 1, x);

        // Else the element can only be present in right subarray
        return binarySearch(arr, mid + 1, high, x);
    }
    return -1;
}

// Driver code
int main() {
    int n;

    // Ask user for the size of the array
    cout << "Enter the number of elements in the array: ";
    cin >> n;

    string arr[n];

    // Ask user to input the elements of the array
    cout << "Enter " << n << " elements (in sorted order): " << endl;
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    string query;
    // Ask user for the value to search
    cout << "Enter the value to search: ";
    cin >> query;

    int result = binarySearch(arr, 0, n - 1, query);
    if (result == -1)
        cout << "Element is not present in array" << endl;
    else
        cout << "Element is present at index " << result << endl;

    return 0;
}