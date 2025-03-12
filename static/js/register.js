$(function(){
	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_check = false;

	$('#user_name').blur(function() {
		check_user_name();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	function check_user_name() {
		var len = $('#user_name').val().length;
	
		if (len < 5 || len > 20) {
			$('#user_name').next().html('Enter a username between 5-20 characters');
			$('#user_name').next().show();
			error_name = true;
		} else {
			$.get('/user/register_exist/?uname=' + $('#user_name').val(), function(data) {
				if (data.count >= 1) {
					$('#user_name').next().html('Username already exists').show();
					error_name = true;
				} else {
					$('#user_name').next().hide();
					error_name = false;
				}
			});
		}
	}

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<4||len>20)
		{
			$('#pwd').next().html('Password must be between 4-20 characters');
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}		
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('Passwords do not match');
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}		
		
	}

	$('#reg_form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();

		if(error_name == false && error_password == false && error_check_password == false && error_check == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});
});


document.addEventListener('DOMContentLoaded', function () {
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