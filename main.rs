
#![allow(warnings)]
fn main() {fn o_type<T>(t: &T) -> String {
    std::any::type_name::<T>().to_string()
}
/* 4 */
let mut name = o_type(&"John");
/* 5 */
name.push(o_type(&"Jane"));
/* 6 */
println!("{:?}", name);

}
        