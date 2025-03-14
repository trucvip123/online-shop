document.addEventListener('DOMContentLoaded', function () {
    if (success) {
        alert("Product saved successfully!");
        window.location.href = successRedirectUrl;
    }
    if (error) {
        alert(error);
    }

    document.getElementById('editProductForm').onsubmit = function () {
        var imagePreviewContainer = document.getElementById('image_preview_container');
        var images = imagePreviewContainer.getElementsByTagName('img');
        for (var i = 0; i < images.length; i++) {
            var hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'image_urls[]';
            hiddenInput.value = images[i].src;
            this.appendChild(hiddenInput);
        }
    };
});

function fetchProductDetails() {
    var productId = document.getElementById('product_id').value;
    if (productId) {
        var xhr = new XMLHttpRequest();
        var form = document.getElementById('editProductForm');
        form.action = editProductHandleUrl + '?product_id=' + productId;

        xhr.open('GET', getProductDetailsUrl + '?product_id=' + encodeURIComponent(productId), true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (!response.error) {
                    document.getElementById('product_name').value = response.product_name;
                    document.getElementById('product_type').value = response.product_type;
                    document.getElementById('brand_name').value = response.brand_name;
                    document.getElementById('price').value = response.price;
                    document.getElementById('price_old').value = response.price_old;
                    document.getElementById('parameter').value = response.parameter;
                    document.getElementById('description').value = response.description;
                    document.getElementById('stock').value = response.stock;
                    updateImagePreview(response.image_urls);
                } else {
                    alert(response.error);
                }
            }
        };
        xhr.send();
    }
}

function updateImagePreview(imageUrls) {
    var imagePreviewContainer = document.getElementById('image_preview_container');
    imagePreviewContainer.innerHTML = '';

    if (imageUrls && imageUrls.length > 0) {
        imageUrls.forEach(function (imageUrl) {
            var wrapper = createImageWrapper(imageUrl);
            imagePreviewContainer.appendChild(wrapper);
        });
    }
    addNewImageInput();
}

function createImageWrapper(imageUrl) {
    var wrapper = document.createElement('div');
    wrapper.className = 'image-wrapper';

    var img = document.createElement('img');
    img.src = imageUrl;

    var button = document.createElement('button');
    button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3 6h18v2H3V6zm2 3h14v13H5V9zm3 2v9h2v-9H8zm4 0v9h2v-9h-2zm4 0v9h2v-9h-2z"/></svg>';
    button.onclick = function () {
        wrapper.remove();
    };

    wrapper.appendChild(img);
    wrapper.appendChild(button);
    return wrapper;
}

function addNewImageInput() {
    var imagePreviewContainer = document.getElementById('image_preview_container');
    var fileInputWrapper = document.createElement('div');
    fileInputWrapper.className = 'image-wrapper';
    var fileInputWrapperInner = document.createElement('div');
    fileInputWrapperInner.className = 'inner-div';
    var fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.id = 'new_image';
    fileInput.name = 'new_image';
    fileInput.multiple = true;
    fileInput.onchange = insertImages;

    var customButton = document.createElement('button');
    customButton.type = 'button';
    customButton.className = 'custom-file-button';
    customButton.onclick = function () {
        fileInput.click();
    };

    fileInputWrapperInner.appendChild(fileInput);
    fileInputWrapperInner.appendChild(customButton);
    fileInputWrapper.appendChild(fileInputWrapperInner);
    imagePreviewContainer.appendChild(fileInputWrapper);
}

function insertImages() {
    var fileInput = document.getElementById('new_image');
    var files = fileInput.files;
    if (files.length > 0) {
        Array.from(files).forEach(function (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var wrapper = createImageWrapper(e.target.result);
                var imagePreviewContainer = document.getElementById('image_preview_container');
                imagePreviewContainer.insertBefore(wrapper, fileInput.parentNode.parentNode);
            };
            reader.readAsDataURL(file);
        });
        fileInput.value = '';
    }
}
