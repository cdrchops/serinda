cd src/rust
cargo build --release
cd ../..
# if linux copy the so
#cp src/rust/target/release/libmylib.dylib ./mylib.so

# if windows copy the dll to the lib directory
cp src/rust/target/release/serindalib.dll ./build/serindalib.dll