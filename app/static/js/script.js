function search() {
    // Get the search term from the input field
    var searchTerm = document.getElementById("searchTerm").value.toLowerCase();

    // Get all the items to be searched
    var items = document.getElementsByClassName("item");

    // Loop through the items and show/hide based on search term
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        var text = item.textContent.toLowerCase();

        if (text.includes(searchTerm)) {
            item.style.display = "block";  // Show item
        } else {
            item.style.display = "none";   // Hide item
        }
    }

    // Show or hide the list based on search results
    var list = document.getElementById("list");
    var listContainer = document.getElementById("list-container");
    if (searchTerm === "") {
        list.classList.add("hidden");  // Hide list
    } else {
        list.classList.remove("hidden");  // Show list
        listContainer.style.display = "block";  // Show list container
    }
}

function selectItem(item) {
    var searchTerm = item.textContent;
    var productId = item.getAttribute("value");
    document.getElementById("searchTerm").value = searchTerm;
    document.getElementById("product_id").value = productId;
    search();
    list.classList.add("hidden");  // Hide list
}