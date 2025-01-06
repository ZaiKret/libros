// Función para confirmar antes de eliminar un libro
document.querySelectorAll('.confirmar-eliminacion').forEach(function(button) {
    button.addEventListener('click', function(event) {
        const confirmation = confirm("¿Estás seguro de que deseas eliminar este libro?");
        if (!confirmation) {
            event.preventDefault();
        }
    });
});
