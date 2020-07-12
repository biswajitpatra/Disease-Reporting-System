new Cleave('.aadhaar',{
    delimiters:['-', '-'],
    delimeterLazyShow: true,
    numericOnly: true,
    blocks: [4,4,4]
});

new Cleave('.mobile',{
    numericOnly: true,
    prefix:'(+91)',
    delimeter:[5,10]
})