import { useState, useEffect } from 'react'
import { supabase } from '../integrations/supabase/client'

function SupabaseDebug() {
    const [stores, setStores] = useState<any[]>([])
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function getStores() {
            try {
                const { data, error } = await (supabase as any)
                    .from('stores')
                    .select('*')
                    .limit(5)

                if (error) {
                    console.error("Supabase error:", error)
                    setError(error.message)
                } else if (data) {
                    setStores(data)
                }
            } catch (err: any) {
                setError(err.message)
            }
        }

        getStores()
    }, [])

    return (
        <div className="p-4">
            <h1 className="text-xl font-bold mb-4">Supabase Connection Debug</h1>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                    Error: {error}
                </div>
            )}

            <div className="space-y-2">
                {stores.length === 0 ? (
                    <p>No stores found (or loading...)</p>
                ) : (
                    stores.map((store) => (
                        <div key={store.store_id} className="p-2 border rounded shadow-sm bg-white">
                            <div className="font-semibold">Store #{store.store_id}</div>
                            <div className="text-sm text-gray-600">{store.location} - {store.size_sqm} sqm</div>
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}

export default SupabaseDebug
