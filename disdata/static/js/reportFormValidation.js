new Cleave('.aadhaar',{
    delimiters:['-', '-'],
    delimeterLazyShow: true,
    numericOnly: true,
    blocks: [4,4,4]
});

new Cleave('.mobile',{
    numericOnly: true,
    prefix:'(+91)',
    blocks: [5,10]
})

new Cleave('#otp',{
    numericOnly: true,
    blocks: [0, 9999]
})

