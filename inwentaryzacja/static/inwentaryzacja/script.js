console.log("dziala");

const number = document.querySelector("#id_kasa_stan");
const div = document.createElement("div");

let d = false;

div.innerHTML = `
  <table border="1" cellpadding="3" cellspacing="0">
    <tr>
      <td>500 zł</td>
      <td><input type="number" class="piecset"></td>
    </tr>
    <tr>
      <td>200 zł</td>
      <td><input type="number" class="dwiescie"></td>
    </tr>
    <tr>
      <td>100 zł</td>
      <td><input type="number" class="sto"></td>
    </tr>
    <tr>
      <td>50 zł</td>
      <td><input type="number" class="piecdziesiat"></td>
    </tr>
    <tr>
      <td>20 zł</td>
      <td><input type="number" class="dwadziescia"></td>
    </tr>
    <tr>
      <td>10 zł</td>
      <td><input type="number" class="dziesiec"></td>
    </tr>
    <tr>
      <td>5 zł</td>
      <td><input type="number" class="piec"></td>
    </tr>
    <tr>
      <td>2 zł</td>
      <td><input type="number" class="dwa"></td>
    </tr>
    <tr>
      <td>1 zł</td>
      <td><input type="number" class="jeden"></td>
    </tr>
    <tr>
      <td>50 gr</td>
      <td><input type="number" class="piec-dziesiatych"></td>
    </tr>
    <tr>
      <td>20 gr</td>
      <td><input type="number" class="dwie-dziesiate"></td>
    </tr>
    <tr>
      <td>10 gr</td>
      <td><input type="number" class="jedna-dziesiata"></td>
    </tr>
    <tr>
      <td>5 gr</td>
      <td><input type="number" class="piec-setnych"></td>
    </tr>
    <tr>
      <td>2 gr</td>
      <td><input type="number" class="dwie-setne"></td>
    </tr>
    <tr>
      <td>1 gr</td>
      <td><input type="number" class="jedna-setna"></td>
    </tr>
    <tr>
      <td colspan="2"><button onClick="oblicz()">Oblicz</button></td>
    </tr>
    <tr>
      <td colspan="2" style="text-align: center;"><small>Created by Sebastian</small></td>
    </tr>
  </table>
`;

number.addEventListener("click", () => {
  console.log('clikc');
  d = !d;
  document.body.appendChild(div);

  if (d) {
    div.style.display = 'block';
  } else {
    div.style.display = 'none';
  }
});

function oblicz() {
  let suma = 0;

  suma += 500 * document.querySelector(".piecset").value;
  suma += 200 * document.querySelector(".dwiescie").value;
  suma += 100 * document.querySelector(".sto").value;
  suma += 50 * document.querySelector(".piecdziesiat").value;
  suma += 20 * document.querySelector(".dwadziescia").value;
  suma += 10 * document.querySelector(".dziesiec").value;
  suma += 5 * document.querySelector(".piec").value;
  suma += 2 * document.querySelector(".dwa").value;
  suma += 1 * document.querySelector(".jeden").value;
  suma += 0.5 * document.querySelector(".piec-dziesiatych").value;
  suma += 0.2 * document.querySelector(".dwie-dziesiate").value;
  suma += 0.1 * document.querySelector(".jedna-dziesiata").value;
  suma += 0.05 * document.querySelector(".piec-setnych").value;
  suma += 0.02 * document.querySelector(".dwie-setne").value;
  suma += 0.01 * document.querySelector(".jedna-setna").value;

  number.value = suma;

  div.style.display = 'none';
}
