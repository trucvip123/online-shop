document.addEventListener('DOMContentLoaded', function () {
    let success = parseInt("{{ success|default:'0' }}", 10);
    if (success === 1) {
        alert("Cập nhật thông tin cá nhân thành công");
    }

    // Toggle form display on "Sửa" button click
    document.getElementById('profile-edit').addEventListener('click', function () {
        const form = document.getElementById('reg_form');
        if (form.style.display === 'none' || form.style.display === '') {
            form.style.display = 'flex';
            document.getElementById('profile-edit').style.display = 'none'
        } else {
            form.style.display = 'none';
        }
    });

    document.getElementById('cancel-edit').addEventListener('click', function () {
        const form = document.getElementById('reg_form');
        if (form.style.display === 'none' || form.style.display === '') {
            form.style.display = 'flex';
        } else {
            form.style.display = 'none';
            document.getElementById('profile-edit').style.display = 'flex'
        }
    });

    document.getElementById('address-insert').addEventListener('click', function () {
        document.getElementById('popup-overlay').style.display = 'block';
        document.getElementById('popup').style.display = 'block';
    });

    document.getElementById('cancel-address').addEventListener('click', function () {
        document.getElementById('popup-overlay').style.display = 'none';
        document.getElementById('popup').style.display = 'none';
    });

    // Address edit buttons
    const addressEditButtons = document.querySelectorAll("#address-edit");
    const addressPopup = document.getElementById("popup");
    const overlay = document.getElementById("popup-overlay");

    addressEditButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Get address details from the clicked address
            const addressContainer = this.closest(".address-detail");
            const addressText = addressContainer.querySelector(".address-detail-info p").textContent;

            // Extract address components (assuming format "Detail, Commune, District, Province")
            const parts = addressText.split(",").map(part => part.trim()); // Loại bỏ khoảng trắng
            const length = parts.length;
            
            if (length >= 4) {
                document.querySelector("[name='province']").value = parts.at(-1) || "";
                document.querySelector("[name='district']").value = parts.at(-2) || "";
                document.querySelector("[name='commune']").value = parts.at(-3) || "";
                document.querySelector("[name='address']").value = parts.slice(0, -3).join(", ") || "";
            }
            

            // Show the popup
            addressPopup.style.display = "block";
            overlay.style.display = "block";
        });
    });

    // Close popup on cancel
    document.getElementById("cancel-address").addEventListener("click", function () {
        addressPopup.style.display = "none";
        overlay.style.display = "none";
    });


    // Fetch provinces
    fetch('https://open.oapi.vn/location/provinces')
        .then(response => response.json())
        .then(data => {
            const provinceSelect = document.getElementById('province');
            provinceSelect.innerHTML = '<option value="">Chọn Tỉnh</option>'; // Default option
            data.data.forEach(province => {
                const option = document.createElement('option');
                option.value = province.id;
                option.textContent = province.name;
                provinceSelect.appendChild(option);
            });

            // Giữ lại tỉnh đã chọn trước đó
            provinceSelect.addEventListener('change', function () {
                let selectedOption = provinceSelect.options[provinceSelect.selectedIndex];
                document.getElementById('province_name').value = selectedOption.textContent;
                fetchDistricts(this.value);
            });
        })
        .catch(error => console.error('Lỗi khi lấy danh sách tỉnh:', error));

    // Xử lý khi chọn tỉnh
    document.getElementById('province').addEventListener('change', function () {
        fetchDistricts(this.value);
    });

    function fetchDistricts(provinceId) {
        if (!provinceId) return;
        fetch(`https://open.oapi.vn/location/districts/${provinceId}`)
            .then(response => response.json())
            .then(data => {
                const districtSelect = document.getElementById('district');
                districtSelect.innerHTML = '<option value="">Chọn Huyện</option>';
                data.data.forEach(district => {
                    const option = document.createElement('option');
                    option.value = district.id;
                    option.textContent = district.name;
                    districtSelect.appendChild(option);
                });

                districtSelect.addEventListener('change', function () {
                    let selectedOption = districtSelect.options[districtSelect.selectedIndex];
                    document.getElementById('district_name').value = selectedOption.textContent;
                    fetchCommunes(this.value);
                });
            })
            .catch(error => console.error('Lỗi khi lấy danh sách huyện:', error));
    }

    // Xử lý khi chọn huyện
    document.getElementById('district').addEventListener('change', function () {
        fetchCommunes(this.value);
    });

    function fetchCommunes(districtId) {
        if (!districtId) return;
        fetch(`https://open.oapi.vn/location/wards/${districtId}`)
            .then(response => response.json())
            .then(data => {
                const communeSelect = document.getElementById('commune');
                communeSelect.innerHTML = '<option value="">Chọn Xã</option>';
                data.data.forEach(commune => {
                    const option = document.createElement('option');
                    option.value = commune.id;
                    option.textContent = commune.name;
                    communeSelect.appendChild(option);
                });

                communeSelect.addEventListener('change', function () {
                    let selectedOption = communeSelect.options[communeSelect.selectedIndex];
                    document.getElementById('commune_name').value = selectedOption.textContent;
                });
            })
            .catch(error => console.error('Lỗi khi lấy danh sách xã:', error));
    }
});