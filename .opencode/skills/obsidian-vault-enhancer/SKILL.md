---
name: obsidian-vault-enhancer
description: Enhance Obsidian markdown files with tags, wikilinks, kebab-case naming, typo fixes, credential cleanup, content expansion, and duplicate detection. Works on user-specified files or entire vault.
compatibility: opencode
metadata:
  audience: obsidian-users
  workflow: note-organization
---

# Obsidian Vault Enhancer

## What I do

I enhance Obsidian markdown files with a comprehensive set of improvements. I work on **user-specified files** or the **entire vault** if no files are provided.

## When to use me

Activate this skill when:
- The user says "mejora [archivo.md]" or "enhance [file.md]"
- The user says "mejora mis apuntes" or "optimize my notes"
- The user wants to organize, clean, or improve Obsidian notes
- The user wants to add tags, wikilinks, fix typos, or rename files

## Activation

```
/mejora archivo1.md archivo2.md
/mejora (sin archivos = vault completa)
```

---

## Mode of Operation: Interactive

**ALWAYS** follow this interaction pattern:

1. **Read** the target file(s) completely
2. **Detect** which improvements apply
3. **Present** a proposal to the user with specific changes
4. **Ask** "¿Aplicar estos cambios?" before each type of change
5. **Show** the diff after applying
6. **Report** summary at the end

**Never apply destructive changes (rename, delete) without explicit confirmation.**

---

## Action 1: Add Obsidian Tags

### What it does
Adds hashtags `#tag1 #tag2 #tag3` below the title of each file for Obsidian's tag system.

### Rules
- Insert tags **below the first `#` title** in the file
- If no title exists, add tags at the very beginning
- Generate **5-8 tags** per file (moderate level)
- Tags are **lowercase**, use hyphens for multi-word: `#react-hook-form`, `#web-security`
- Tags cover: technologies, concepts, categories, relationships

### Process
1. Read the file content
2. Identify main topics, technologies, concepts
3. Generate relevant tags in format `#tag1 #tag2 #tag3`
4. Insert below the title
5. Show the user what tags will be added
6. Apply after confirmation

### Tag naming conventions
- Programming languages: `#javascript`, `#python`, `#c`
- Frameworks: `#react`, `#vite`, `#tailwind-css`
- Concepts: `#web-security`, `#pentesting`, `#backend`
- Tools: `#docker`, `#nmap`, `#redis`
- Categories: `#cheatsheet`, `#writeup`, `#tutorial`

---

## Action 2: Add Internal Wikilinks

### What it does
Creates `[[wikilinks]]` between related notes to enable Obsidian's graph view and navigation.

### Rules
- Scan file content for mentions of technologies/concepts that exist as notes
- Scan entire vault to build a list of available note names
- Create wikilinks: `[[note-name]]` or `[[note-name|display text]]`
- Connect notes within the same category
- Add "Notas relacionadas" section at the end if many connections exist
- If files are specified, only link to those files AND any notes they reference
- If no files specified (full vault mode), link across all notes

### Process
1. Build index of all note names in the vault (or specified files)
2. Scan target file for mentions of other notes' topics
3. Create natural wikilinks within the text
4. Add related notes section if appropriate
5. Show user the links to be created
6. Apply after confirmation

### Link examples
- `XSS.md` mentions SOP → add `[[Vocabulary]]`
- `React Notes.md` discusses forms → add `[[React Hook Form & Zod]]`
- `cap.md` uses Nmap → add `[[Nmap cheatsheet]]`
- `Proxmox.md` mentions containers → add `[[Alpine-Linux]]`

---

## Action 3: Rename to Kebab-Case

### What it does
Standardizes filenames to kebab-case (lowercase, hyphens, no special characters).

### Rules
- Spaces → hyphens: `React Notes.md` → `react-notes.md`
- Lowercase everything: `Redis cheatsheet.md` → `redis-cheatsheet.md`
- Remove special characters: `&`, commas, tildes in filenames
- Preserve `.md` extension
- **CRITICAL**: After renaming, update ALL wikilinks across the entire vault that reference the old name

### Characters to remove
- `&` → remove
- `,` → remove
- Spaces → `-`
- Uppercase → lowercase
- Tildes/accents → remove (filenames only, preserve in content)

### Process
1. List current filename
2. Show proposed new name
3. Ask for confirmation (destructive change)
4. Rename file
5. Search entire vault for old filename references
6. Update all wikilinks
7. Show summary of all changes

---

## Action 4: Fix Typos and Spelling

### What it does
Corrects common spelling errors in Spanish text.

### Common errors dictionary
| Error | Correction |
|-------|-----------|
| atraves | a través |
| protecion | protección |
| malloria | mayoría |
| ejecuyte | ejecute |
| arbritario | arbitrario |
| indiscriminiado | indiscriminado |
| cualuier | cualquier |
| completmanete | completamente |
| cosisntencia | consistencia |
| restaurara | restaurar |
| inciativas | iniciativas |
| utlidad | utilidad |
| desdeada | deseada |
| servier | server |
| reconcen | reconocen |
| domino | dominio |
| regsitrarme | registrarme |
| Policiy | Policy |

### Rules
- Only fix obvious typos, never change technical terms
- Preserve code blocks unchanged
- Preserve URLs unchanged
- Preserve proper nouns unchanged
- Show user each correction before applying

---

## Action 5: Clean Credentials

### What it does
Redacts exposed tokens, passwords, and API keys from markdown files.

### Patterns to detect
- ngrok tokens: long alphanumeric strings after `authtoken`
- Docker passwords: `SFTP_USERS=user:password:uid`
- Writeup credentials: `PASS: password`, `user y password`
- API keys: patterns like `sk-`, `ghp_`, `Bearer`
- Any string that looks like a real credential

### Process
1. Scan file for credential patterns
2. List each found credential with line number
3. **ALWAYS** ask user before redacting (security change)
4. Replace with `[REDACTED]` or `[credential]`
5. Show before/after diff
6. Warn about security implications

---

## Action 6: Expand Incomplete Notes

### What it does
Fills in placeholder content and expands very short notes.

### Detection criteria
- Files containing only "TODO", "To DO", "Pendiente"
- Files with less than 10 lines of content
- Sections with headers but no content below them
- Placeholder text like "Aquí irá la documentación..."

### Process
1. Detect incomplete notes
2. Show user which notes are incomplete
3. Ask which ones to expand
4. Generate relevant content matching the note's style
5. Maintain existing format (headers, code blocks, callouts)
6. Add wikilinks to expanded content
7. Show diff before applying

---

## Action 7: Detect and Resolve Duplicates

### What it does
Identifies duplicated content between files and proposes solutions.

### Detection method
- Compare file contents for similar paragraphs
- Identify sections that appear in multiple files
- Flag files with >70% content overlap

### Resolution options
1. **Remove duplicate + add wikilink**: Keep the more complete version, link from the other
2. **Merge content**: Combine both versions into one
3. **Keep both**: If they serve different purposes, just add cross-links

### Process
1. Scan for content similarity
2. Present duplicates to user
3. Propose resolution strategy
4. Ask for confirmation
5. Execute with wikilinks

---

## Action 8: Translate to Spanish

### What it does
Translates non-Spanish text to Spanish while preserving technical terms.

### Rules
- Only translate clearly non-Spanish sections (Catalan, English prose)
- Never translate: code, command names, technology names, file paths
- Never translate: technical jargon that's commonly used in English
- Preserve markdown formatting

---

## Action 9: Create MOCs (Maps of Content)

### What it does
Creates index notes that link to all notes in a category.

### Only in full vault mode
MOCs are only created when working on the entire vault, not individual files.

### MOC structure
```markdown
#category #moc

# Category - Map of Content

Brief description of this category.

## Subcategory 1
- [[note-1]] - Brief description
- [[note-2]] - Brief description

## Subcategory 2
- [[note-3]] - Brief description

## Notas Relacionadas
- [[other-category/moc]]
```

---

## Workflow Summary

```
1. Receive file list from user (or scan entire vault)
2. For EACH file:
   a. Read complete content
   b. Detect which improvements apply
   c. Present proposal to user
   d. Ask: "¿Aplicar estos cambios?"
   e. If yes → apply and show diff
   f. If no → skip
3. For renames: update ALL wikilinks in vault
4. At end: summary report of all changes
```

## Important Notes

- **Always work in the vault root directory** specified by the user
- **Preserve markdown formatting** - never break code blocks, callouts, or tables
- **Respect user's style** - match existing tone and formatting
- **Security first** - always ask before redacting credentials
- **Destructive changes** - always confirm before rename/delete
- **Spanish as default** - unless user specifies otherwise
