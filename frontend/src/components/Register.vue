<script setup></script>
<template>
    <form action="POST">
        <h2>Register</h2>
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" minlength="8" required>
    </form>
</template>
<style>
</style>