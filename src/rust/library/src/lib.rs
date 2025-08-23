//https://erambler.co.uk/blog/extending-python-rust-1/
//https://michaeljung.dev/2017/11/12/passing-strings-from-python-to-rust/
// http://jakegoulding.com/rust-ffi-omnibus/string_arguments/
use std::ffi::CStr;
use std::os::raw::c_char;

#[no_mangle]
pub fn add(a: i64, b: i64) -> i64 {
    a + b
}

#[no_mangle]
pub fn print_something(s: *const c_char) {
   let c_str = unsafe {
        assert!(!s.is_null());

        CStr::from_ptr(s)
    };

    let r_str = c_str.to_str().unwrap();

    println!("{:?}", r_str);
    println!("helloworld... I am death, destroyer of worlds... and DAVY JONES GIANT SQUID!");
}

#[no_mangle]
pub extern "C" fn how_many_characters(s: *const c_char) -> u32 {
    let c_str = unsafe {
        assert!(!s.is_null());

        CStr::from_ptr(s)
    };

    let r_str = c_str.to_str().unwrap();
    r_str.chars().count() as u32
}