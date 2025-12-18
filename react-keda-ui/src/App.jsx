// import { useState } from 'react'

// function App() {
//   const [status, setStatus] = useState('')

//   const sendMessage = async () => {
//     setStatus('Sending...')
//     try {
//       const response = await fetch(
//         'https://function300.azurewebsites.net/api/send?code=hxaJ8E2cSCzkaqIqF2TzYzgqSGseCKdlYaFGjG-uZg2oAzFuKWdX_g==',
//         {
//           method: 'POST',
//           headers: { 'Content-Type': 'application/json' },
//           body: JSON.stringify({ message: 'Message from React button!' }),
//         }
//       )

//       if (response.ok) {
//         setStatus('✅ Message sent successfully!')
//       } else {
//         const error = await response.text()
//         setStatus(`❌ Error: ${error}`)
//       }
//     } catch (err) {
//       setStatus(`❌ Request failed: ${err.message}`)
//     }
//   }

//   return (
//     <div style={{ padding: 40, textAlign: 'center' }}>
//       <h1>React + Azure Function Queue Trigger</h1>
//       <button onClick={sendMessage} style={{ fontSize: 18, padding: '10px 20px' }}>
//         Send Queue Message
//       </button>
//       <p>{status}</p>
//     </div>
//   )
// }

// export default App
import { useState } from 'react'

const PRODUCTS = [
  { id: 1, name: 'Wireless Mouse', price: 25, quantity: 10 },
  { id: 2, name: 'Mechanical Keyboard', price: 75, quantity: 5 },
  { id: 3, name: 'HD Monitor', price: 150, quantity: 3 },
]

function App() {
  const [status, setStatus] = useState('')
  const [products] = useState(PRODUCTS)

  const buyProduct = async (product) => {
    setStatus(`Sending order for ${product.name}...`)
    try {
      const response = await fetch(
        'https://function300.azurewebsites.net/api/send?code=hxaJ8E2cSCzkaqIqF2TzYzgqSGseCKdlYaFGjG-uZg2oAzFuKWdX_g==',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: `Order placed: ${product.name}, $${product.price}`,
          }),
        }
      )

      if (response.ok) {
        setStatus(`✅ Order sent for ${product.name}!`)
      } else {
        const error = await response.text()
        setStatus(`❌ Error: ${error}`)
      }
    } catch (err) {
      setStatus(`❌ Request failed: ${err.message}`)
    }
  }

  return (
    <div style={{ padding: 20, textAlign: 'left' }}>
      <h1>🛒 Online Store</h1>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 40 }}>
        {products.map((p) => (
          <div key={p.id} style={{ border: '1px solid #ccc', padding: 20, borderRadius: 8 }}>
            <h3>{p.name}</h3>
            <p>Price: ${p.price}</p>
            <p>Stock: {p.quantity}</p>
            <button onClick={() => buyProduct(p)}>Buy</button>
          </div>
        ))}
      </div>
      <p style={{ marginTop: 20 }}>{status}</p>
    </div>
  )
}

export default App
