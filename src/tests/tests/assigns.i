a = 0;
b = 1;
a = b;
c = 2.5;
d = "Hola";
e = d;

f = [1, 2, 3];
a = f[1];
b = f[2];

g = [1, a, 2, b, 3];
g[a] = b;
g[b] = a;

h = [f[g[a]], g[g[b]]];
h[f[g[a]]] = g[f[g[g[b]]]];

c1 = "2+2=4;";
c2 = "if (c) then ... else ...";
c3 = "# Este no es un comentario";
