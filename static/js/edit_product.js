document.addEventListener('DOMContentLoaded', function () {
    const formId = document.getElementById('editProductForm') ? 'editProductForm' : 'addProductForm';

    document.getElementById(formId).onsubmit = function () {
        updateHiddenInputs(formId);
    };

    const imageInput = document.getElementById('image_input');
    if (imageInput) {
        imageInput.addEventListener('change', previewSelectedImages);
    }

    enableDragAndDrop();
});

function updateHiddenInputs(formId) {
    const imagePreviewContainer = document.getElementById('image_preview_container');
    const images = imagePreviewContainer.querySelectorAll('.image-wrapper img');

    // Clear existing hidden inputs
    document.querySelectorAll('input[name="image_urls[]"]').forEach(input => input.remove());

    // Add hidden inputs for the reordered images
    images.forEach(img => {
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'image_urls[]';
        hiddenInput.value = img.src;
        document.getElementById(formId).appendChild(hiddenInput);
    });

    console.log("Updated image order submitted:");
    images.forEach((img, index) => {
        console.log(`Image ${index + 1}: ${img.src}`);
    });
}

function fetchProductDetails() {
    const productId = document.getElementById('product_id').value;
    if (productId) {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `${getProductDetailsUrl}?product_id=${encodeURIComponent(productId)}`, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
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
    const imagePreviewContainer = document.getElementById('image_preview_container');
    imagePreviewContainer.innerHTML = '';

    if (imageUrls && imageUrls.length > 0) {
        imageUrls.forEach(imageUrl => {
            const wrapper = createImageWrapper(imageUrl);
            imagePreviewContainer.appendChild(wrapper);
        });
    }
    addNewImageInput();
}

function createImageWrapper(imageUrl) {
    const wrapper = document.createElement('div');
    wrapper.className = 'image-wrapper';

    const img = document.createElement('img');
    img.src = imageUrl;

    const button = document.createElement('button');
    button.type = 'button'; // Ensure the button does not submit the form
    button.className = 'remove-image-button';
    button.innerHTML = 'Remove';
    button.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent any default action
        wrapper.remove(); // Properly remove the wrapper
    });

    wrapper.appendChild(img);
    wrapper.appendChild(button);
    return wrapper;
}

function addNewImageInput() {
    const imagePreviewContainer = document.getElementById('image_preview_container');
    const fileInputWrapper = document.createElement('div');
    fileInputWrapper.className = 'image-wrapper';
    const fileInputWrapperInner = document.createElement('div');
    fileInputWrapperInner.className = 'inner-div';
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.id = 'new_image';
    fileInput.name = 'new_image';
    fileInput.multiple = true;
    fileInput.onchange = insertImages;

    const customButton = document.createElement('button');
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
    const fileInput = document.getElementById('new_image');
    const files = fileInput.files;
    if (files.length > 0) {
        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = function (e) {
                const wrapper = createImageWrapper(e.target.result);
                const imagePreviewContainer = document.getElementById('image_preview_container');
                imagePreviewContainer.insertBefore(wrapper, fileInput.parentNode.parentNode);
            };
            reader.readAsDataURL(file);
        });
        fileInput.value = '';
    }
}

function enableDragAndDrop() {
    const container = document.getElementById('image_preview_container');
    let draggedItem = null;
    let placeholder = null;
    let offsetX = 0;
    let offsetY = 0;

    container.addEventListener('pointerdown', function (e) {
        if (e.target.closest('.image-wrapper')) {
            draggedItem = e.target.closest('.image-wrapper');
            const rect = draggedItem.getBoundingClientRect();
            offsetX = e.clientX - rect.left;
            offsetY = e.clientY - rect.top;

            placeholder = document.createElement('div');
            placeholder.className = 'placeholder';
            placeholder.style.height = `${draggedItem.offsetHeight}px`;
            placeholder.style.width = `${draggedItem.offsetWidth}px`;
            placeholder.style.border = '2px dashed #007bff';
            container.insertBefore(placeholder, draggedItem.nextSibling);

            draggedItem.style.position = 'absolute';
            draggedItem.style.zIndex = '1000';
            draggedItem.style.pointerEvents = 'none';
            draggedItem.style.transition = 'none'; // Disable transition during drag
            moveDraggedItem(e.clientX, e.clientY);
        }
    });

    container.addEventListener('pointermove', function (e) {
        if (draggedItem) {
            moveDraggedItem(e.clientX, e.clientY);

            const target = document.elementFromPoint(e.clientX, e.clientY)?.closest('.image-wrapper');
            if (target && target !== draggedItem && target !== placeholder) {
                const bounding = target.getBoundingClientRect();
                const offset = bounding.y + bounding.height / 2;
                if (e.clientY > offset) {
                    container.insertBefore(placeholder, target.nextSibling);
                } else {
                    container.insertBefore(placeholder, target);
                }
            }
        }
    });

    container.addEventListener('pointerup', function () {
        if (draggedItem) {
            container.insertBefore(draggedItem, placeholder);
            draggedItem.style.position = '';
            draggedItem.style.zIndex = '';
            draggedItem.style.pointerEvents = '';
            draggedItem.style.transition = 'all 0.3s ease'; // Smooth transition back to position
            draggedItem.style.top = '';
            draggedItem.style.left = '';
            placeholder.remove();

            // Log the updated order of images after drag-and-drop
            const images = container.querySelectorAll('.image-wrapper img');
            console.log("Updated image order after drag-and-drop:");
            images.forEach((img, index) => {
                console.log(`Image ${index + 1}: ${img.src}`);
            });

            draggedItem = null;
            placeholder = null;
        }
    });

    function moveDraggedItem(clientX, clientY) {
        draggedItem.style.top = `${clientY - offsetY}px`;
        draggedItem.style.left = `${clientX - offsetX}px`;
    }
}

function previewSelectedImages(event) {
    const files = event.target.files;
    const imagePreviewContainer = document.getElementById('image_preview_container');
    imagePreviewContainer.innerHTML = ''; // Clear existing previews

    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = function (e) {
            const wrapper = createImageWrapper(e.target.result);
            imagePreviewContainer.appendChild(wrapper);
        };
        reader.readAsDataURL(file);
    });
}
