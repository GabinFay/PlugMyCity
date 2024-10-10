<?php
// Check if the address is set in the POST data (after MetaMask connection)
if (isset($_POST['address'])) {
    $address = $_POST['address'];
    // Redirect to the Streamlit app with the address as a parameter
    header("Location: http://localhost:8501/?address=" . urlencode($address));
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MetaMask Test</title>
    <!-- Lien vers le fichier CSS -->
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <div class="wrapper">
        <header>
            <h1 class="title">PlugMyCity</h1>
        </header>

        <div class="container">
            <button id="connectButton">Connect to MetaMask</button>
        </div>
    <script>
        document.getElementById('connectButton').addEventListener('click', async () => {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    // Request account access
                    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                    const address = accounts[0];
                    
                    // Submit the address to the PHP script
                    const form = document.createElement('form');
                    form.method = 'post';
                    form.innerHTML = `<input name="address" value="${address}">`;
                    document.body.append(form);
                    form.submit();
                } catch (error) {
                    console.error('User denied account access');
                }
            } else {
                console.log('MetaMask not detected');
            }
        });
    </script>
</body>

</html>
