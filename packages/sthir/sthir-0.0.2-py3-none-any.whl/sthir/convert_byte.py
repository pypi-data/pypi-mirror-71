from bitarray import bitarray
import base64

HTML_TEMPLATE = {
    "HEAD":
    """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <pre id="demo"></pre>
            <script>
                !function(a,b){"use strict";function c(a,b){return(65535&a)*b+(((a>>>16)*b&65535)<<16)}function d(a,b){return a<<b|a>>>32-b}function e(a){return a^=a>>>16,a=c(a,2246822507),a^=a>>>13,a=c(a,3266489909),a^=a>>>16}function f(a,b){a=[a[0]>>>16,65535&a[0],a[1]>>>16,65535&a[1]],b=[b[0]>>>16,65535&b[0],b[1]>>>16,65535&b[1]];var c=[0,0,0,0];return c[3]+=a[3]+b[3],c[2]+=c[3]>>>16,c[3]&=65535,c[2]+=a[2]+b[2],c[1]+=c[2]>>>16,c[2]&=65535,c[1]+=a[1]+b[1],c[0]+=c[1]>>>16,c[1]&=65535,c[0]+=a[0]+b[0],c[0]&=65535,[c[0]<<16|c[1],c[2]<<16|c[3]]}function g(a,b){a=[a[0]>>>16,65535&a[0],a[1]>>>16,65535&a[1]],b=[b[0]>>>16,65535&b[0],b[1]>>>16,65535&b[1]];var c=[0,0,0,0];return c[3]+=a[3]*b[3],c[2]+=c[3]>>>16,c[3]&=65535,c[2]+=a[2]*b[3],c[1]+=c[2]>>>16,c[2]&=65535,c[2]+=a[3]*b[2],c[1]+=c[2]>>>16,c[2]&=65535,c[1]+=a[1]*b[3],c[0]+=c[1]>>>16,c[1]&=65535,c[1]+=a[2]*b[2],c[0]+=c[1]>>>16,c[1]&=65535,c[1]+=a[3]*b[1],c[0]+=c[1]>>>16,c[1]&=65535,c[0]+=a[0]*b[3]+a[1]*b[2]+a[2]*b[1]+a[3]*b[0],c[0]&=65535,[c[0]<<16|c[1],c[2]<<16|c[3]]}function h(a,b){return b%=64,32===b?[a[1],a[0]]:32>b?[a[0]<<b|a[1]>>>32-b,a[1]<<b|a[0]>>>32-b]:(b-=32,[a[1]<<b|a[0]>>>32-b,a[0]<<b|a[1]>>>32-b])}function i(a,b){return b%=64,0===b?a:32>b?[a[0]<<b|a[1]>>>32-b,a[1]<<b]:[a[1]<<b-32,0]}function j(a,b){return[a[0]^b[0],a[1]^b[1]]}function k(a){return a=j(a,[0,a[0]>>>1]),a=g(a,[4283543511,3981806797]),a=j(a,[0,a[0]>>>1]),a=g(a,[3301882366,444984403]),a=j(a,[0,a[0]>>>1])}var l={version:"3.0.1",x86:{},x64:{}};l.x86.hash32=function(a,b){a=a||"",b=b||0;for(var f=a.length%4,g=a.length-f,h=b,i=0,j=3432918353,k=461845907,l=0;g>l;l+=4)i=255&a.charCodeAt(l)|(255&a.charCodeAt(l+1))<<8|(255&a.charCodeAt(l+2))<<16|(255&a.charCodeAt(l+3))<<24,i=c(i,j),i=d(i,15),i=c(i,k),h^=i,h=d(h,13),h=c(h,5)+3864292196;switch(i=0,f){case 3:i^=(255&a.charCodeAt(l+2))<<16;case 2:i^=(255&a.charCodeAt(l+1))<<8;case 1:i^=255&a.charCodeAt(l),i=c(i,j),i=d(i,15),i=c(i,k),h^=i}return h^=a.length,h=e(h),h>>>0},l.x86.hash128=function(a,b){a=a||"",b=b||0;for(var f=a.length%16,g=a.length-f,h=b,i=b,j=b,k=b,l=0,m=0,n=0,o=0,p=597399067,q=2869860233,r=951274213,s=2716044179,t=0;g>t;t+=16)l=255&a.charCodeAt(t)|(255&a.charCodeAt(t+1))<<8|(255&a.charCodeAt(t+2))<<16|(255&a.charCodeAt(t+3))<<24,m=255&a.charCodeAt(t+4)|(255&a.charCodeAt(t+5))<<8|(255&a.charCodeAt(t+6))<<16|(255&a.charCodeAt(t+7))<<24,n=255&a.charCodeAt(t+8)|(255&a.charCodeAt(t+9))<<8|(255&a.charCodeAt(t+10))<<16|(255&a.charCodeAt(t+11))<<24,o=255&a.charCodeAt(t+12)|(255&a.charCodeAt(t+13))<<8|(255&a.charCodeAt(t+14))<<16|(255&a.charCodeAt(t+15))<<24,l=c(l,p),l=d(l,15),l=c(l,q),h^=l,h=d(h,19),h+=i,h=c(h,5)+1444728091,m=c(m,q),m=d(m,16),m=c(m,r),i^=m,i=d(i,17),i+=j,i=c(i,5)+197830471,n=c(n,r),n=d(n,17),n=c(n,s),j^=n,j=d(j,15),j+=k,j=c(j,5)+2530024501,o=c(o,s),o=d(o,18),o=c(o,p),k^=o,k=d(k,13),k+=h,k=c(k,5)+850148119;switch(l=0,m=0,n=0,o=0,f){case 15:o^=a.charCodeAt(t+14)<<16;case 14:o^=a.charCodeAt(t+13)<<8;case 13:o^=a.charCodeAt(t+12),o=c(o,s),o=d(o,18),o=c(o,p),k^=o;case 12:n^=a.charCodeAt(t+11)<<24;case 11:n^=a.charCodeAt(t+10)<<16;case 10:n^=a.charCodeAt(t+9)<<8;case 9:n^=a.charCodeAt(t+8),n=c(n,r),n=d(n,17),n=c(n,s),j^=n;case 8:m^=a.charCodeAt(t+7)<<24;case 7:m^=a.charCodeAt(t+6)<<16;case 6:m^=a.charCodeAt(t+5)<<8;case 5:m^=a.charCodeAt(t+4),m=c(m,q),m=d(m,16),m=c(m,r),i^=m;case 4:l^=a.charCodeAt(t+3)<<24;case 3:l^=a.charCodeAt(t+2)<<16;case 2:l^=a.charCodeAt(t+1)<<8;case 1:l^=a.charCodeAt(t),l=c(l,p),l=d(l,15),l=c(l,q),h^=l}return h^=a.length,i^=a.length,j^=a.length,k^=a.length,h+=i,h+=j,h+=k,i+=h,j+=h,k+=h,h=e(h),i=e(i),j=e(j),k=e(k),h+=i,h+=j,h+=k,i+=h,j+=h,k+=h,("00000000"+(h>>>0).toString(16)).slice(-8)+("00000000"+(i>>>0).toString(16)).slice(-8)+("00000000"+(j>>>0).toString(16)).slice(-8)+("00000000"+(k>>>0).toString(16)).slice(-8)},l.x64.hash128=function(a,b){a=a||"",b=b||0;for(var c=a.length%16,d=a.length-c,e=[0,b],l=[0,b],m=[0,0],n=[0,0],o=[2277735313,289559509],p=[1291169091,658871167],q=0;d>q;q+=16)m=[255&a.charCodeAt(q+4)|(255&a.charCodeAt(q+5))<<8|(255&a.charCodeAt(q+6))<<16|(255&a.charCodeAt(q+7))<<24,255&a.charCodeAt(q)|(255&a.charCodeAt(q+1))<<8|(255&a.charCodeAt(q+2))<<16|(255&a.charCodeAt(q+3))<<24],n=[255&a.charCodeAt(q+12)|(255&a.charCodeAt(q+13))<<8|(255&a.charCodeAt(q+14))<<16|(255&a.charCodeAt(q+15))<<24,255&a.charCodeAt(q+8)|(255&a.charCodeAt(q+9))<<8|(255&a.charCodeAt(q+10))<<16|(255&a.charCodeAt(q+11))<<24],m=g(m,o),m=h(m,31),m=g(m,p),e=j(e,m),e=h(e,27),e=f(e,l),e=f(g(e,[0,5]),[0,1390208809]),n=g(n,p),n=h(n,33),n=g(n,o),l=j(l,n),l=h(l,31),l=f(l,e),l=f(g(l,[0,5]),[0,944331445]);switch(m=[0,0],n=[0,0],c){case 15:n=j(n,i([0,a.charCodeAt(q+14)],48));case 14:n=j(n,i([0,a.charCodeAt(q+13)],40));case 13:n=j(n,i([0,a.charCodeAt(q+12)],32));case 12:n=j(n,i([0,a.charCodeAt(q+11)],24));case 11:n=j(n,i([0,a.charCodeAt(q+10)],16));case 10:n=j(n,i([0,a.charCodeAt(q+9)],8));case 9:n=j(n,[0,a.charCodeAt(q+8)]),n=g(n,p),n=h(n,33),n=g(n,o),l=j(l,n);case 8:m=j(m,i([0,a.charCodeAt(q+7)],56));case 7:m=j(m,i([0,a.charCodeAt(q+6)],48));case 6:m=j(m,i([0,a.charCodeAt(q+5)],40));case 5:m=j(m,i([0,a.charCodeAt(q+4)],32));case 4:m=j(m,i([0,a.charCodeAt(q+3)],24));case 3:m=j(m,i([0,a.charCodeAt(q+2)],16));case 2:m=j(m,i([0,a.charCodeAt(q+1)],8));case 1:m=j(m,[0,a.charCodeAt(q)]),m=g(m,o),m=h(m,31),m=g(m,p),e=j(e,m)}return e=j(e,[0,a.length]),l=j(l,[0,a.length]),e=f(e,l),l=f(l,e),e=k(e),l=k(l),e=f(e,l),l=f(l,e),("00000000"+(e[0]>>>0).toString(16)).slice(-8)+("00000000"+(e[1]>>>0).toString(16)).slice(-8)+("00000000"+(l[0]>>>0).toString(16)).slice(-8)+("00000000"+(l[1]>>>0).toString(16)).slice(-8)},"undefined"!=typeof exports?("undefined"!=typeof module&&module.exports&&(exports=module.exports=l),exports.murmurHash3=l):"function"==typeof define&&define.amd?define([],function(){return l}):(l._murmurHash3=a.murmurHash3,l.noConflict=function(){return a.murmurHash3=l._murmurHash3,l._murmurHash3=b,l.noConflict=b,l},a.murmurHash3=l)}(this);

                class bitArray {
                    constructor(base64, chunk_size, m, no_hashes) {
                        this.bit_array = atob(base64);
                        this.length = this.bit_array.length;
                        this.chunk_size = chunk_size;
                        this.m = m;
                        this.no_hashes = no_hashes;
                    }
                    get(n) {
                        let x = (2**(8-(n%8) - 1))
                        n = Math.floor(n/8);
                        let num = this.bit_array.charCodeAt(n);
                        // console.log(n, x, num);
                        if (String(num & x) != String(0)) {
                            return true;
                        }
                        else {
                            return false;
                        }
                    }
                    get_range(n, m) {
                        let curr = "";

                        for (var i=n; i<m; i++) {
                            let x = (2**(8-(i%8) - 1));
                            let j = Math.floor(i/8);
                            let num = this.bit_array.charCodeAt(j);
                            // console.log(j, x, num);
                            if (String(num & x) != String(0)) {
                                curr += "1";
                            }
                            else {
                                curr += "0";
                            }
                        }
                        return curr;
                    }
                    get_chunk(n) {
                        let m = this.chunk_size*(n+1);
                        n = m - this.chunk_size;

                        let curr = "";

                        for (var i=n; i<m; i++) {
                            let x = (2**(8-(i%8) - 1));
                            let j = Math.floor(i/8);
                            let num = this.bit_array.charCodeAt(j);
                            // console.log(j, x, num);
                            if (String(num & x) != String(0)) {
                                curr += "1";
                            }
                            else {
                                curr += "0";
                            }
                        }
                        return curr;
                    }
                    get_hashes(word) {
                        let hash_indices = []
                        for (var i = 0; i < this.no_hashes; i++){
                            // console.log(murmurHash3.x86.hash32(word, i));
                            hash_indices.push( murmurHash3.x86.hash32(word, i) % this.m );
                        }
                        return hash_indices;
                    }
                    bin_to_integer(bool_string){
                        let integer  = 0;
                        bool_string = bool_string.split('').reverse().join('');
                        for(var i = bool_string.length-1 ; i >=0  ; i--) {
                            if(bool_string.charAt(i) == "1") {
                                integer += Math.pow( 2 , i);
                            }
                        }
                        return integer;
                    }                    
                    get_all_chunks(word, get_min) {
                        let hash_indices = this.get_hashes(word);
                        let vals = []
                        for (var i = 0; i < hash_indices.length; i++) {
                            vals.push(this.bin_to_integer(this.get_chunk(hash_indices[i])));
                        }
                        if (get_min == false) {
                            return vals;
                        }
                        else if (get_min == true) {
                            return Math.min.apply(Math, vals);
                        }
                    }
                    get_document_score(words, get_sum) {
                        let score = 0;
                        let scores = []
                        for(var i = 0; i < words.length; i++) {
                            let curr_score = this.get_all_chunks(words[i], true);
                            score += curr_score;
                            scores.push(score);
                        }
                        if (get_sum == true) {
                            return score;
                        }
                        else if (get_sum == false) {
                            return scores;
                        }
                    }
                }

                let demo = document.getElementById("demo");
        """,
    "TAIL":
    """
            let bit_arr = new bitArray("{}", 4, 14474, 3);
            // console.log(bit_arr.get_range(0, 50));
            demo.innerHTML = bit_arr.bit_array;
            </script>
        </body>
        </html>
        """
}
if __name__ == "__main__":
    bit_arr = bitarray()
    with open("document.bin", "rb") as f:
        bit_arr.fromfile(f)
    print(len(bit_arr))
    b64 = base64.b64encode(bit_arr.tobytes())
    with open("output.html","w") as f:
        f.write(HTML_TEMPLATE["HEAD"])
        f.write(HTML_TEMPLATE["TAIL"].format(b64.decode()))