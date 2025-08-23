cd src/rust
cargo build --release
cd ../..
# if linux copy the so
cp src/rust/target/release/libserindalib.so ./build/serindalib.so

# if windows copy the dll to the lib directory
copy .\src\rust\target\release\serindalib.dll .\build\serindalib.dll