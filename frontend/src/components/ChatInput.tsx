import { useState, useRef } from 'react';
import { Send, ImagePlus, X } from 'lucide-react';

interface Props {
  onSend: (message: string, image?: string) => void;
  loading: boolean;
}

export default function ChatInput({ onSend, loading }: Props) {
  const [text, setText] = useState('');
  const [image, setImage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if ((!text.trim() && !image) || loading) return;
    onSend(text.trim(), image || undefined);
    setText('');
    setImage(null);
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setImage(reader.result as string);
    };
    reader.readAsDataURL(file);

    // Reset input so same file can be re-selected
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border-t border-zinc-800 bg-zinc-900/80 backdrop-blur p-4">
      {/* Image preview */}
      {image && (
        <div className="mb-3 relative inline-block">
          <img
            src={image}
            alt="Preview"
            className="max-w-[180px] max-h-[120px] rounded-lg border border-zinc-700 object-contain"
          />
          <button
            type="button"
            onClick={() => setImage(null)}
            className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
          >
            <X size={12} />
          </button>
        </div>
      )}

      <div className="flex items-end gap-2">
        {/* Image upload button */}
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="p-2.5 rounded-lg text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-colors"
          title="Subir imagen"
        >
          <ImagePlus size={20} />
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          className="hidden"
        />

        {/* Text input */}
        <div className="flex-1 relative">
          <textarea
            value={text}
            onChange={e => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Pregunta sobre Cobblemon... (Enter para enviar, Shift+Enter para nueva línea)"
            rows={1}
            className="w-full bg-zinc-800 text-zinc-100 rounded-xl px-4 py-2.5 pr-10 text-sm placeholder-zinc-500 border border-zinc-700 focus:border-indigo-500 focus:outline-none resize-none transition-colors"
            disabled={loading}
          />
        </div>

        {/* Send button */}
        <button
          type="submit"
          disabled={loading || (!text.trim() && !image)}
          className="p-2.5 rounded-lg bg-indigo-600 text-white hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all shrink-0"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <Send size={20} />
          )}
        </button>
      </div>
    </form>
  );
}
