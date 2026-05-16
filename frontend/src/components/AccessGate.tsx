import { useState } from 'react';
import { Cherry, Lock } from 'lucide-react';

interface Props {
  onUnlock: () => void;
}

export default function AccessGate({ onUnlock }: Props) {
  const [code, setCode] = useState('');
  const [error, setError] = useState(false);
  const [checking, setChecking] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!code.trim()) return;

    setChecking(true);
    setError(false);

    try {
      const res = await fetch('/api/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_code: code }),
      });

      if (res.ok) {
        sessionStorage.setItem('cobblemon_access', code);
        onUnlock();
      } else {
        setError(true);
      }
    } catch {
      setError(true);
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-950 p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-emerald-700 flex items-center justify-center mx-auto mb-4">
            <Cherry size={28} />
          </div>
          <h1 className="text-lg font-semibold text-zinc-100">Cobblemon DeepAgent</h1>
          <p className="text-sm text-zinc-500 mt-1">Acceso restringido</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
            <input
              type="password"
              value={code}
              onChange={e => { setCode(e.target.value); setError(false); }}
              placeholder="Código de acceso"
              className="w-full bg-zinc-900 text-zinc-100 rounded-xl pl-10 pr-4 py-3 text-sm border border-zinc-800 focus:border-emerald-500 focus:outline-none transition-colors"
              autoFocus
              disabled={checking}
            />
          </div>

          {error && (
            <p className="text-red-400 text-xs text-center">Código incorrecto</p>
          )}

          <button
            type="submit"
            disabled={checking || !code.trim()}
            className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-xl py-3 text-sm font-medium transition-colors"
          >
            {checking ? 'Verificando...' : 'Entrar'}
          </button>
        </form>
      </div>
    </div>
  );
}
