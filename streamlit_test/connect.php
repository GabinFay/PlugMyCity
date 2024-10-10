<?php
$data = json_decode(file_get_contents('php://input'), true);
$account = $data['account'];
// Process MetaMask account here (e.g., store in database)
echo json_encode(['status' => 'connected', 'account' => $account]);
?>
