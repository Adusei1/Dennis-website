const multiSelect =document.getElementByld('multiSelect');

const selectedValues =new Set();

 multiSelect.addEventListener('click',()=> {
     multiSelect.classList.toggle('active');
 });

 dropdown.addEventListener('click',(e) => {
    const value = e.target.getAttribute('data-value');
    const lable = e.target.textContent;

    if(!selectedValues.has(value)) {
       selectedValues.add(value);

       const tag =document.createElement('span');
       tag.innerHTML = 'S{label} <i data-remove="S{values}">&times;</i>';
       selectedItems.appendChild(tag);
    }
});

selectedItems.addEventListener('click',(e) => {
     if(e.target.dataset.remove) {
         const valueToRemove = e.target.dataset.remove;
         selectedValues.delete(valueToRemove);
         e.target.parentElement.remove(); 
     }
});
