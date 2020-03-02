const username = $('label[for=id_username]');
const password = $('label[for=id_password]');
const placeholderUsername = $('#id_username');
const placeholderPassword = $('#id_password');
const oldPassword = $('label[for=id_old_password]');
const newPassword = $('label[for=id_new_password1]');
const newPasswordConfirm = $('label[for=id_new_password2]');
const placeholderOldPassword = $('#id_old_password');
const placeholderNewPassword = $('#id_new_password1');
const placeholderNewPasswordConfirm = $('#id_new_password2');
const listItem1 = $('small.form-text ul li:first-child');
const listItem2 = $('small.form-text ul li:nth-child(2n)');
const listItem3 = $('small.form-text ul li:nth-child(3n)');
const listItem4 = $('small.form-text ul li:last-child');

// Login
username.text('Nazwa Użytkownika');
password.text('Hasło');

placeholderUsername.attr({
  placeholder: "Nazwa Użytkownika"
});

placeholderPassword.attr({
  placeholder: "Hasło"
});



// Change Password
oldPassword.text("Stare Hasło");
newPassword.text("Nowe Hasło");
newPasswordConfirm.text("Potwierdzenie Nowego Hasła");

placeholderOldPassword.attr({
  placeholder: "Stare Hasło"
});

placeholderNewPassword.attr({
  placeholder: "Nowe Hasło"
});

placeholderNewPasswordConfirm.attr({
  placeholder: "Potwierdzenie Nowego Hasła"
});

listItem1.text("Twoje hasło nie może być zbyt podobne do innych danych osobowych.");
listItem2.text("Twoje hasło musi zawierać co najmniej 8 znaków.");
listItem3.text("Twoje hasło nie może być powszechnie używanym hasłem.");
listItem4.text("Twoje hasło nie może być całkowicie numeryczne.");
