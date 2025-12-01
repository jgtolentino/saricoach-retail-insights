import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'

function SupabaseDebug() {
    const [stores, setStores] = useState<any[]>([])
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function getStores() {
            try {
                // Query the 'stores' table in the 'kaggle' schema (or public if you exposed it)
                // Note: supabase-js client usually defaults to 'public' schema.
                // If tables are in 'kaggle' schema, we might need to adjust or use a view in public.
                // For now, let's try selecting from 'kaggle.stores' if the client supports it, 
                // or assume we might need to expose it. 
                // Actually, the seed script creates 'kaggle.stores'. 
                // Let's try to query it. If it fails, we'll see the error.

                const { data, error } = await supabase
                    .from('stores') // This assumes public schema or exposed view
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
