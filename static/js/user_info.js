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

    document.getElementById('cancel-edit-address').addEventListener('click', function () {
        document.getElementById('popup-overlay').style.display = 'none';
        document.getElementById('edit-popup').style.display = 'none';
    });

    // Address edit buttons
    const addressEditButtons = document.querySelectorAll("#address-edit");
    const addressPopup = document.getElementById("edit-popup");
    const overlay = document.getElementById("popup-overlay");

    addressEditButtons.forEach(button => {
        button.addEventListener("click", async function () {
            const addressContainer = this.closest(".address-detail");
            const addressText = addressContainer.querySelector(".address-detail-info p").textContent;

            // Tách các phần của địa chỉ
            const parts = addressText.split(",").map(part => part.trim());
            if (parts.length < 4) return;

            const [detail, commune, district, province] = [
                parts.slice(0, -3).join(", "),
                parts.at(-3),
                parts.at(-2),
                parts.at(-1)
            ];
            document.querySelector("[name='address-detail']").value = detail;
            try {
                // Lấy danh sách tỉnh từ API
                const provinces = await fetchProvinces();
                const provinceSelect = document.getElementById('edit_province');
                provinceSelect.innerHTML = '<option value="">Chọn Tỉnh</option>';
                provinces.forEach(province => {
                    const option = document.createElement('option');
                    option.value = province.id;
                    option.textContent = province.name;
                    provinceSelect.appendChild(option);
                });

                const selectedProvince = provinces.find(p => p.name === province);
                if (selectedProvince) {
                    provinceSelect.value = selectedProvince.id;
                    await fetchDistricts(selectedProvince.id, district, commune);
                }
            } catch (error) {
                console.error("Lỗi khi lấy dữ liệu địa chỉ:", error);
            }

            // Hiển thị popup
            addressPopup.style.display = "block";
            overlay.style.display = "block";
        });
    });

    async function fetchProvinces() {
        const response = await fetch('https://open.oapi.vn/location/provinces');
        const data = await response.json();
        return data.data || [];
    }

    async function fetchDistricts(provinceId, selectedDistrict, selectedCommune) {
        if (!provinceId) return;
        const response = await fetch(`https://open.oapi.vn/location/districts/${provinceId}`);
        const data = await response.json();
        const districts = data.data || [];

        const districtSelect = document.getElementById('edit_district');
        districtSelect.innerHTML = '<option value="">Chọn Huyện</option>';
        districts.forEach(district => {
            const option = document.createElement('option');
            option.value = district.id;
            option.textContent = district.name;
            districtSelect.appendChild(option);
        });

        const selectedDistrictObj = districts.find(d => d.name === selectedDistrict);
        if (selectedDistrictObj) {
            districtSelect.value = selectedDistrictObj.id;
            await fetchCommunes(selectedDistrictObj.id, selectedCommune);
        }
    }

    async function fetchCommunes(districtId, selectedCommune) {
        if (!districtId) return;
        const response = await fetch(`https://open.oapi.vn/location/wards/${districtId}`);
        const data = await response.json();
        const communes = data.data || [];

        const communeSelect = document.getElementById('edit_commune');
        communeSelect.innerHTML = '<option value="">Chọn Xã</option>';
        communes.forEach(commune => {
            const option = document.createElement('option');
            option.value = commune.id;
            option.textContent = commune.name;
            communeSelect.appendChild(option);
        });

        const selectedCommuneObj = communes.find(c => c.name === selectedCommune);
        if (selectedCommuneObj) {
            communeSelect.value = selectedCommuneObj.id;
        }
    }

    document.querySelectorAll('#address-delete').forEach(function(button) {
        button.addEventListener('click', function() {
            const addressElement = this.closest('.address-detail-element');
            const addressId = addressElement.querySelector('p').getAttribute('id');

            if (confirm('Bạn có chắc chắn muốn xóa địa chỉ này?')) {
                fetch(`/user/delete_user_address/${addressId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        addressElement.remove();
                    } else {
                        alert('Đã xảy ra lỗi khi xóa địa chỉ.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Đã xảy ra lỗi khi xóa địa chỉ.');
                });
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
     cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
