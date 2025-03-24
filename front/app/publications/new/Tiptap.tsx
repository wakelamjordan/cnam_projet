"use client";

import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Link from "@tiptap/extension-link";
import Heading from "@tiptap/extension-heading";

const Tiptap = () => {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Link.configure({ openOnClick: true }),
      Heading.configure({ levels: [2, 3, 4, 5, 6] }),
    ],
    content: "<p>Commencez à écrire ici...</p>",
  });

  if (!editor) {
    return null;
  }

  return (
    <div className="border p-4 rounded-lg">
      {/* Barre d'outils */}
      <div className="mb-2 flex gap-2">
        <button
          onClick={() => editor.chain().focus().toggleBold().run()}
          className={`px-2 py-1 border ${
            editor.isActive("bold") ? "bg-gray-200" : ""
          }`}
        >
          Bold
        </button>
        <button
          onClick={() => editor.chain().focus().toggleItalic().run()}
          className={`px-2 py-1 border ${
            editor.isActive("italic") ? "bg-gray-200" : ""
          }`}
        >
          Italic
        </button>
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 2 }).run()
          }
          className={`px-2 py-1 border ${
            editor.isActive("heading", { level: 2 }) ? "bg-gray-200" : ""
          }`}
        >
          H2
        </button>
        <button
          onClick={() =>
            editor.chain().focus().toggleHeading({ level: 3 }).run()
          }
          className={`px-2 py-1 border ${
            editor.isActive("heading", { level: 3 }) ? "bg-gray-200" : ""
          }`}
        >
          H3
        </button>
        <button
          onClick={() => {
            const url = prompt("Entrez l'URL du lien:");
            if (url) editor.chain().focus().setLink({ href: url }).run();
          }}
          className="px-2 py-1 border"
        >
          Add Link
        </button>
        <button
          onClick={() => editor.chain().focus().unsetLink().run()}
          className="px-2 py-1 border"
        >
          Remove Link
        </button>
      </div>

      {/* Zone d'édition */}
      <EditorContent
        editor={editor}
        className="border p-2 rounded-md min-h-[200px]"
      />
    </div>
  );
};

export default Tiptap;
