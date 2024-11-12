
#![allow(warnings)]
fn main() {
fn o_type<T>(t: &T) -> String {
    std::any::type_name::<T>().to_string()
}
let mut name = "Hello, World!";
println!("{:?}", o_type(&name.to_string()));
println!("{:?}", name);
}
        