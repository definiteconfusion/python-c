
#![allow(warnings)]
fn main() {
fn o_type<T>(t: &T) -> String {
    std::any::type_name::<T>().to_string()
}
let mut strnum = "123";
let mut num: i32 = 123;
println!("{}", o_type(&strnum));
println!("{}", o_type(&num.to_string()));
}
        