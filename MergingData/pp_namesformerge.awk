function shut(list){
    if(close(list)){
	print list "failed to close" > "/dev/stderr";
    }
}
BEGIN{

#file = "./data/origstops.txt"
file = ARGV[1];
FS = ","

while((getline < file) > 0){
    print substr($1, 1, 3) ", "  "\"" $3 "\""
}
shut(file)

}
