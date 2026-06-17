# BioVault — Build Strategy & Step-by-Step Game Plan
**Created: June 14, 2026**
**Product: Blockchain-Anchored Personal Biometric Data Platform with Patient-Owned Digital Wallet**

---

## PRODUCT OVERVIEW

BioVault anchors personal biometric data to a distributed ledger (DLT), giving patients an immutable, cryptographically verified health record that they own and control through a digital wallet. Data is stored encrypted off-chain; only cryptographic hashes are anchored on-chain.

## TECH STACK (DECIDED)

- **Backend:** Rust (Axum) — enterprise-grade, memory-safe
- **DLT Integration:** Canton Network (primary), Solana (secondary/consumer-facing)
- **Smart Contracts:** Canton (enterprise), Solana Anchor (consumer)
- **Off-Chain Storage:** Encrypted NAS (Ubiquiti UNAS-2 with 48TB Seagate Exos)
- **Cryptography:** SHA-256 hashing, AES-256-GCM encryption, Ed25519 signing
- **Wallet:** Patient-facing web wallet + mobile-responsive

## ARCHITECTURE

```
[Biometric Data Input]
         ↓
[Encrypted Off-Chain Storage (NAS)]
         ↓
[SHA-256 Hash Computation]
         ↓
┌────────────────┐
│  DLT Anchoring │ → Canton Network (enterprise/private)
│                │ → Solana (consumer/public)
│                │ → Any DLT (future-proof)
└────────────────┘
         ↓
[Patient Digital Wallet]
  ├─ View anchored health data
  ├─ Grant/revoke provider access
  ├─ Longitudinal timeline
  └─ Research participation (opt-in)
```

---

## PHASE 1: Core Infrastructure & Storage (Weeks 1-3)

**PREREQUISITE: NAS hardware delivered and configured (June 16/22/23)**

### Step 1: NAS Setup & Encryption
- Install Ubiquiti UNAS-2 with 2x Seagate Exos 24TB drives
- Configure RAID (RAID 1 for redundancy or RAID 0 for capacity — decide based on backup strategy)
- Enable AES-256 full-disk encryption
- Configure Ubiquiti Cloud Gateway for remote access management
- Set up secure network segmentation (separate VLAN for health data)
- Document physical security controls for HIPAA

### Step 2: Off-Chain Encrypted Storage Layer
- Build Rust storage service that accepts biometric data
- Encrypt all incoming data with AES-256-GCM before write
- Implement patient-specific key derivation (each patient's data encrypted with unique derived key)
- Build secure read/decrypt pathway (requires patient wallet authorization)
- Implement audit logging (every read/write/decrypt operation logged)

### Step 3: Hashing & Verification Module
- Implement SHA-256 hash computation for all stored biometric data
- Build verification service: given data + anchored hash → verify match
- Implement Merkle tree construction for batch anchoring efficiency
- Build hash index (off-chain database mapping patient → hash → DLT transaction)

---

## PHASE 2: DLT Anchoring Integration (Weeks 3-5)

### Step 4: Canton Network Integration
- Set up Canton Network node or connect to existing node infrastructure
- Implement Canton transaction submission for hash anchoring
- Build transaction confirmation monitoring
- Test anchoring with sample data hashes
- **Show raw anchoring results → Report to Enoch**

### Step 5: Solana Integration (Consumer Layer)
- Set up Solana RPC connection
- Implement Solana transaction for hash anchoring (memo or custom program)
- Build consumer-facing transaction explorer links (patients can see their anchors on Solana explorer)
- Test with devnet first, then mainnet
- **Show raw test results → Report to Enoch**

### Step 6: Multi-DLT Abstraction Layer
- Build DLT abstraction trait/interface in Rust:
  ```
  trait DLTAnchor {
    async fn anchor_hash(&self, hash: &str, metadata: &AnchorMetadata) -> Result<TxReceipt>;
    async fn verify_anchor(&self, hash: &str) -> Result<VerificationProof>;
    async fn get_anchor_timestamp(&self, tx_hash: &str) -> Result<Timestamp>;
  }
  ```
- Implement for Canton, Solana
- Design for extensibility — any future DLT can be added by implementing the trait

---

## PHASE 3: Patient Digital Wallet (Weeks 5-7)

### Step 7: Wallet Core
- Build Ed25519 keypair generation and management
- Implement patient wallet creation flow
- Build wallet authentication (sign-in with wallet credentials)
- Implement key recovery mechanisms (social recovery, custodial backup)

### Step 8: Access Management
- Build access grant/revoke system (patient authorizes provider)
- Implement time-limited access tokens
- Build selective sharing (specific data types only)
- Implement provider access directory (who has access, to what, until when)

### Step 9: Health Timeline UI
- Build chronological display of all anchored biometric data
- Show DLT verification badges (confirmed on Canton/Solana at [timestamp])
- Build before/after comparison view (longitudinal tracking)
- Show therapeutic effectiveness scores when paired with PepPrint data

---

## PHASE 4: Smart Contracts & Research Module (Weeks 7-9)

### Step 10: Access Policy Smart Contracts
- Deploy smart contracts on Canton for programmatic access policies
- Implement time-limited provider access contracts
- Implement emergency access contracts
- Implement multi-signature authorization for critical operations

### Step 11: Research Data Marketplace
- Build patient opt-in flow for research participation
- Implement de-identification verification (Smart Contract verifies Safe Harbor compliance before release)
- Build researcher query interface
- Implement compensation distribution via smart contract
- Test with sample research queries

### Step 12: Testing & Security Audit
- Full end-to-end testing of anchoring → wallet → access management flow
- Security audit of cryptographic implementations
- Penetration testing on storage layer
- **Pre-flight check → Show results → Report to Enoch**

---

## PHASE 5: Integration & Launch (Weeks 9-10)

### Step 13: PepPrint Integration
- Connect PepPrint AI analysis reports to BioVault anchoring
- Every PepPrint report gets anchored to DLT
- Patient wallet shows PepPrint reports alongside raw biomarker data
- Longitudinal tracking combines PepPrint analysis across time

### Step 14: Provider Access Integration
- Providers access BioVault data through PepPrint Pro portal
- Patient-initiated access grant flows to provider dashboard
- Audit trail visible to both patient and provider

### Step 15: Launch Readiness
- Complete documentation
- HIPAA compliance verification (if operating in Mode I)
- Performance testing under load
- Disaster recovery testing
- **Final launch review → Report to Enoch and George**

---

## BUILD PIPELINE (SAME AS PepPrint)

1. Claude Code (DeepSeek V4 Pro proxy) builds → show raw output
2. Tests → show raw results
3. If fail → back to Claude Code
4. Pre-flight check → show results
5. Report to Enoch at each phase boundary

## KEY DEPENDENCIES

- **NAS delivery:** June 16 (Cloud Gateway), June 22 (Drives), June 23 (NAS enclosure)
- **Canton Network access:** Need to establish node or partner connection
- **Solana RPC:** Free tier for devnet, paid for mainnet
- **HIPAA compliance:** Parallel track — Compliancy Group or similar for Mode I operation
- **PepPrint MVP:** BioVault Phase 5 depends on PepPrint being operational

## DLT STRATEGY

| DLT | Role | Why |
|-----|------|-----|
| **Canton Network** | Enterprise/private anchoring | Privacy-preserving, institutional-grade, DTCC partnership, preferred for identified PHI data |
| **Solana** | Consumer-facing anchoring | Fast, cheap, public explorers let patients see their anchors, good for wallet UX |
| **Hedera (future)** | Enterprise alternative | If Canton adoption stalls, Hedera provides similar enterprise governance |

## FILE LOCATIONS

- Code: `bits/biovault/`
- Patent: Desktop + Obsidian `patents/BioVault-Provisional-Patent.md`
- This strategy: Desktop + Obsidian

---

## SEQUENCING SUMMARY

```
Week 1-2:  PepPrint Phase 1 (biomarker DB + AI engine)
Week 2-3:  PepPrint Phase 2 (upload + PDF parsing)
Week 3-4:  PepPrint Phase 3 (reports + patient portal) | BioVault Phase 1 starts (NAS setup)
Week 4-5:  PepPrint Phase 4 (provider portal) | BioVault Phase 1 continues
Week 5-7:  PepPrint LAUNCH | BioVault Phase 2-3 (DLT anchoring + wallet)
Week 7-9:  BioVault Phase 4 (smart contracts + research)
Week 9-10: BioVault Phase 5 (integration + launch)
```

**Total timeline: ~10 weeks from NAS delivery to full BioVault launch.**
PepPrint MVP in ~4-5 weeks. BioVault in ~10 weeks.
