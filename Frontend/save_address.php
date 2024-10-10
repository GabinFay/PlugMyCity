<?php
session_start();

if (isset($_POST['address'])) {
    $_SESSION['user_address'] = $_POST['address'];
    echo "Address saved successfully";
} else {
    echo "No address provided";
}